from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from product.models import Product, Category
from core_ecommerce.models import Order, OrderItem
from core_ecommerce.forms import CheckoutForm
from collections import defaultdict
from decimal import Decimal


class HomeView(View):
    template_name = 'home/index.html'
    products_per_page = 12

    def get(self, request):
        categories = Category.objects.all()
        search_query = request.GET.get('q', '')
        selected_category_slug = request.GET.get('category', '')
        
        # Get all products or filter by search/category
        products = Product.objects.select_related('category', 'vendor').all()
        
        if search_query:
            products = products.filter(name__icontains=search_query)
        
        if selected_category_slug:
            products = products.filter(category__slug=selected_category_slug)
        
        # Group products by category
        products_by_category = defaultdict(list)
        for product in products:
            if product.category:
                category_key = (product.category.name, product.category.slug)
            else:
                category_key = ('Uncategorized', 'uncategorized')
            products_by_category[category_key].append(product)
        
        # Convert to list of tuples for template
        category_rows = []
        for (category_name, category_slug), category_products in sorted(products_by_category.items()):
            # Paginate products for each category
            paginator = Paginator(category_products, self.products_per_page)
            page = request.GET.get(f'page_{category_slug}', 1)
            
            try:
                paginated_products = paginator.page(page)
            except PageNotAnInteger:
                paginated_products = paginator.page(1)
            except EmptyPage:
                paginated_products = paginator.page(paginator.num_pages)
            
            category_rows.append({
                'category_name': category_name,
                'category_slug': category_slug,
                'products': paginated_products,
                'paginator': paginator,
            })
        
        context = {
            'categories': categories,
            'category_rows': category_rows,
            'search_query': search_query,
            'selected_category': selected_category_slug,
        }
        return render(request, self.template_name, context)


def get_cart(request):
    """Helper function to get cart from session"""
    cart = request.session.get('cart', {})
    return cart


def get_cart_items(request):
    """Helper function to get cart items with product details"""
    cart = get_cart(request)
    cart_items = []
    total = Decimal('0.00')
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.select_related('category', 'vendor').get(id=int(product_id))
            item_total = product.price * Decimal(str(quantity))
            total += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })
        except Product.DoesNotExist:
            # Remove invalid product from cart
            cart.pop(product_id, None)
            request.session['cart'] = cart
            request.session.modified = True
    
    return cart_items, total


def get_cart_count(request):
    """Helper function to get total number of items in cart"""
    cart = get_cart(request)
    return sum(cart.values())


class AddToCartView(View):
    """Add product to cart"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
        
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart[product_id_str] += quantity
        else:
            cart[product_id_str] = quantity
        
        request.session['cart'] = cart
        request.session.modified = True
        
        messages.success(request, f'{product.name} added to cart!')
        
        # Redirect back to product detail or referrer
        redirect_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
        return redirect(redirect_url)


class CartView(View):
    """View cart contents"""
    template_name = 'cart/cart.html'
    
    def get(self, request):
        cart_items, total = get_cart_items(request)
        
        context = {
            'cart_items': cart_items,
            'total': total,
            'cart_count': get_cart_count(request),
        }
        return render(request, self.template_name, context)


class UpdateCartView(View):
    """Update cart item quantity"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        if quantity < 1:
            # Remove item if quantity is 0 or less
            cart.pop(product_id_str, None)
            messages.info(request, f'{product.name} removed from cart.')
        else:
            cart[product_id_str] = quantity
            messages.success(request, f'{product.name} quantity updated.')
        
        request.session['cart'] = cart
        request.session.modified = True
        
        return redirect('core_ecommerce:cart')


class RemoveFromCartView(View):
    """Remove product from cart"""
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = get_cart(request)
        product_id_str = str(product_id)
        
        if product_id_str in cart:
            cart.pop(product_id_str, None)
            request.session['cart'] = cart
            request.session.modified = True
            messages.success(request, f'{product.name} removed from cart.')
        
        return redirect('core_ecommerce:cart')


class ClearCartView(View):
    """Clear entire cart"""
    
    def post(self, request):
        request.session['cart'] = {}
        request.session.modified = True
        messages.info(request, 'Cart cleared.')
        return redirect('core_ecommerce:cart')


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    """Checkout view to process orders"""
    template_name = 'checkout/checkout.html'
    
    def get(self, request):
        # Check if cart is empty
        cart_items, total = get_cart_items(request)
        if not cart_items:
            messages.warning(request, 'Your cart is empty. Add items to cart before checkout.')
            return redirect('core_ecommerce:cart')
        
        form = CheckoutForm(user=request.user)
        
        context = {
            'form': form,
            'cart_items': cart_items,
            'subtotal': total,
            'shipping_cost': Decimal('0.00'),  # Can be calculated based on location
            'total': total,
            'cart_count': get_cart_count(request),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # Check if cart is empty
        cart_items, subtotal = get_cart_items(request)
        if not cart_items:
            messages.warning(request, 'Your cart is empty. Add items to cart before checkout.')
            return redirect('core_ecommerce:cart')
        
        form = CheckoutForm(request.POST, user=request.user)
        
        if form.is_valid():
            # Calculate shipping (can be enhanced with shipping logic)
            shipping_cost = Decimal('0.00')
            total = subtotal + shipping_cost
            
            # Create order
            order = Order.objects.create(
                customer=request.user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                shipping_address=form.cleaned_data['shipping_address'],
                billing_address=form.cleaned_data.get('billing_address') or form.cleaned_data['shipping_address'],
                city=form.cleaned_data['city'],
                region=form.cleaned_data.get('region', ''),
                postal_code=form.cleaned_data.get('postal_code', ''),
                country=form.cleaned_data.get('country', 'Ethiopia'),
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                total=total,
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price,
                    subtotal=item['item_total'],
                )
            
            # Clear cart after successful order
            request.session['cart'] = {}
            request.session.modified = True
            
            messages.success(request, f'Order placed successfully! Order number: {order.order_number}')
            return redirect('core_ecommerce:order_success', order_id=order.id)
        
        # Form is invalid, show errors
        context = {
            'form': form,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_cost': Decimal('0.00'),
            'total': subtotal,
            'cart_count': get_cart_count(request),
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class OrderSuccessView(View):
    """Order success confirmation page"""
    template_name = 'checkout/order_success.html'
    
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        context = {
            'order': order,
        }
        return render(request, self.template_name, context)