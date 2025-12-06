from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import hashlib
import secrets

from .models import Store, Product, Cart, CartItem, Order, OrderItem, Review, ResetToken
from .forms import (
    UserRegistrationForm, StoreForm, ProductForm, ReviewForm,
    PasswordResetRequestForm, PasswordResetForm
)


# Authentication Views
def register_user(request):
    """Handle user registration with vendor/buyer account types"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            account_type = form.cleaned_data['account_type']

            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Assign to appropriate group
            if account_type == 'vendor':
                group, created = Group.objects.get_or_create(name='Vendors')
                user.groups.add(group)
                messages.success(request, 'Vendor account created successfully!')
            else:
                group, created = Group.objects.get_or_create(name='Buyers')
                user.groups.add(group)
                messages.success(request, 'Buyer account created successfully!')

            # Create cart for buyer
            if account_type == 'buyer':
                Cart.objects.get_or_create(user=user)

            # Auto login
            login(request, user)
            return redirect('ecommerce:home')
    else:
        form = UserRegistrationForm()

    return render(request, 'ecommerce/register.html', {'form': form})


def login_user(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('ecommerce:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'ecommerce/login.html')


@login_required
def logout_user(request):
    """Handle user logout"""
    # Clear session cart
    if 'cart' in request.session:
        del request.session['cart']
    messages.success(request, 'You have been logged out successfully.')
    from django.contrib.auth import logout
    logout(request)
    return redirect('ecommerce:login')


# Password Reset Views
def generate_reset_url(user, request):
    """Generate secure reset token and URL"""
    # Generate random token
    random_token = secrets.token_urlsafe(32)
    # Hash it for storage
    token_hash = hashlib.sha1(random_token.encode()).hexdigest()

    # Create reset token record
    expiry_date = timezone.now() + timedelta(minutes=30)
    ResetToken.objects.create(
        user=user,
        token=token_hash,
        expiry_date=expiry_date
    )

    # Generate reset URL
    reset_url = request.build_absolute_uri(f'/ecommerce/reset-password/{random_token}/')
    return reset_url


def send_reset_email(user, reset_url):
    """Send password reset email"""
    subject = 'Password Reset Request'
    message = f'''
    Hello {user.username},

    You requested a password reset for your account.

    Please click the following link to reset your password:
    {reset_url}

    This link will expire in 30 minutes.

    If you did not request this, please ignore this email.

    Best regards,
    Ecommerce Team
    '''
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def request_password_reset(request):
    """Handle password reset request"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            # Generate reset URL
            reset_url = generate_reset_url(user, request)

            # Send email
            if send_reset_email(user, reset_url):
                messages.success(request, 'Password reset link has been sent to your email.')
            else:
                messages.error(request, 'Failed to send email. Please try again later.')
            return redirect('ecommerce:login')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'ecommerce/password_reset_request.html', {'form': form})


def reset_user_password(request, token):
    """Handle password reset with token"""
    if request.user.is_authenticated:
        return redirect('ecommerce:home')

    # Hash the token to compare
    token_hash = hashlib.sha1(token.encode()).hexdigest()

    try:
        reset_token = ResetToken.objects.get(token=token_hash)
        if not reset_token.is_valid():
            messages.error(request, 'Invalid or expired reset token.')
            return redirect('ecommerce:request_password_reset')

        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                # Set new password
                user = reset_token.user
                user.set_password(form.cleaned_data['password'])
                user.save()

                # Mark token as used
                reset_token.used = True
                reset_token.save()

                messages.success(request, 'Password reset successfully! Please login with your new password.')
                return redirect('ecommerce:login')
        else:
            form = PasswordResetForm()

        return render(request, 'ecommerce/password_reset.html', {'form': form, 'token': token})

    except ResetToken.DoesNotExist:
        messages.error(request, 'Invalid reset token.')
        return redirect('ecommerce:request_password_reset')


# Vendor Store Views
@login_required
def create_store(request):
    """Create a new store (vendor only)"""
    if not request.user.groups.filter(name='Vendors').exists():
        messages.error(request, 'Only vendors can create stores.')
        return redirect('ecommerce:home')

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            messages.success(request, 'Store created successfully!')
            return redirect('ecommerce:my_stores')
    else:
        form = StoreForm()

    return render(request, 'ecommerce/store_form.html', {'form': form})


@login_required
def my_stores(request):
    """Display vendor's stores"""
    if not request.user.groups.filter(name='Vendors').exists():
        messages.error(request, 'Only vendors can view stores.')
        return redirect('ecommerce:home')

    stores = Store.objects.filter(owner=request.user)
    return render(request, 'ecommerce/my_stores.html', {'stores': stores})


@login_required
def edit_store(request, store_id):
    """Edit store (owner only)"""
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        messages.error(request, 'You do not have permission to edit this store.')
        return redirect('ecommerce:my_stores')

    if request.method == 'POST':
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, 'Store updated successfully!')
            return redirect('ecommerce:my_stores')
    else:
        form = StoreForm(instance=store)

    return render(request, 'ecommerce/store_form.html', {'form': form, 'store': store})


@login_required
def delete_store(request, store_id):
    """Delete store (owner only)"""
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        messages.error(request, 'You do not have permission to delete this store.')
        return redirect('ecommerce:my_stores')

    if request.method == 'POST':
        store.delete()
        messages.success(request, 'Store deleted successfully!')
        return redirect('ecommerce:my_stores')

    return render(request, 'ecommerce/store_confirm_delete.html', {'store': store})


# Vendor Product Views
@login_required
def add_product(request, store_id):
    """Add product to store (store owner only)"""
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        messages.error(request, 'You do not have permission to add products to this store.')
        return redirect('ecommerce:my_stores')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('ecommerce:store_products', store_id=store_id)
    else:
        form = ProductForm()

    return render(request, 'ecommerce/product_form.html', {'form': form, 'store': store})


@login_required
def store_products(request, store_id):
    """Display products in a store"""
    store = get_object_or_404(Store, id=store_id)

    if store.owner != request.user:
        messages.error(request, 'You do not have permission to view this store.')
        return redirect('ecommerce:my_stores')

    products = Product.objects.filter(store=store)
    return render(request, 'ecommerce/store_products.html', {'store': store, 'products': products})


@login_required
def edit_product(request, product_id):
    """Edit product (product owner only)"""
    product = get_object_or_404(Product, id=product_id)

    if product.store.owner != request.user:
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('ecommerce:my_stores')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('ecommerce:store_products', store_id=product.store.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'ecommerce/product_form.html', {'form': form, 'product': product})


@login_required
def delete_product(request, product_id):
    """Delete product (product owner only)"""
    product = get_object_or_404(Product, id=product_id)

    if product.store.owner != request.user:
        messages.error(request, 'You do not have permission to delete this product.')
        return redirect('ecommerce:my_stores')

    store_id = product.store.id

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('ecommerce:store_products', store_id=store_id)

    return render(request, 'ecommerce/product_confirm_delete.html', {'product': product})


# Buyer Views
def home(request):
    """Display all products"""
    products = Product.objects.all()
    return render(request, 'ecommerce/home.html', {'products': products})


def browse_products(request):
    """Display available products (stock > 0)"""
    products = Product.objects.filter(stock__gt=0)
    return render(request, 'ecommerce/browse_products.html', {'products': products})


def product_detail(request, product_id):
    """Show product details with reviews"""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    can_review = False

    if request.user.is_authenticated:
        # Check if user can review (hasn't reviewed yet and is a buyer)
        if request.user.groups.filter(name='Buyers').exists():
            can_review = not Review.objects.filter(product=product, buyer=request.user).exists()

    return render(request, 'ecommerce/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'can_review': can_review
    })


@login_required
def add_to_cart(request, product_id):
    """Add product to cart"""
    if request.method != 'POST':
        messages.error(request, 'Invalid request method.')
        return redirect('ecommerce:product_detail', product_id=product_id)
    
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can add items to cart.')
        return redirect('ecommerce:home')

    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        messages.error(request, 'Invalid quantity.')
        return redirect('ecommerce:product_detail', product_id=product_id)

    if quantity <= 0:
        messages.error(request, 'Invalid quantity.')
        return redirect('ecommerce:product_detail', product_id=product_id)

    if quantity > product.stock:
        messages.error(request, 'Not enough stock available.')
        return redirect('ecommerce:product_detail', product_id=product_id)

    # Get or create cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add to database cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('ecommerce:product_detail', product_id=product_id)
        cart_item.save()

    # Also store in session as backup
    if 'cart' not in request.session:
        request.session['cart'] = {}

    cart_dict = request.session['cart']
    cart_dict[str(product_id)] = cart_dict.get(str(product_id), 0) + quantity
    request.session['cart'] = cart_dict
    request.session.modified = True

    messages.success(request, f'{product.name} added to cart!')
    return redirect('ecommerce:view_cart')


@login_required
def view_cart(request):
    """Display cart items"""
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can view cart.')
        return redirect('ecommerce:home')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Sync session cart with database cart
    if 'cart' in request.session:
        session_cart = request.session['cart']
        for product_id, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                if product.stock > 0:
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=cart,
                        product=product,
                        defaults={'quantity': min(quantity, product.stock)}
                    )
                    if not created:
                        cart_item.quantity = min(cart_item.quantity + quantity, product.stock)
                        cart_item.save()
            except Product.DoesNotExist:
                pass
        # Clear session cart after sync
        del request.session['cart']

    cart_items = CartItem.objects.filter(cart=cart)
    total = cart.get_total()

    return render(request, 'ecommerce/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can modify cart.')
        return redirect('ecommerce:home')

    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user != request.user:
        messages.error(request, 'You do not have permission to remove this item.')
        return redirect('ecommerce:view_cart')

    product_id = cart_item.product.id
    cart_item.delete()

    # Also remove from session
    if 'cart' in request.session:
        cart_dict = request.session['cart']
        if str(product_id) in cart_dict:
            del cart_dict[str(product_id)]
            request.session['cart'] = cart_dict
            request.session.modified = True

    messages.success(request, 'Item removed from cart.')
    return redirect('ecommerce:view_cart')


def send_invoice_email(order):
    """Generate and send invoice email"""
    subject = f'Order Confirmation - Order #{order.id}'
    message = f'''
    Hello {order.buyer.username},

    Thank you for your order!

    Order Details:
    Order ID: #{order.id}
    Date: {order.created_at.strftime("%Y-%m-%d %H:%M:%S")}
    Status: {order.get_status_display()}

    Items:
    '''
    for item in order.items.all():
        message += f'\n- {item.product_name} x{item.quantity} @ ${item.price} = ${item.get_subtotal()}'

    message += f'''
    
    Total Amount: ${order.total_amount}

    We will process your order shortly.

    Best regards,
    Ecommerce Team
    '''

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.buyer.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending invoice email: {e}")
        return False


@login_required
@transaction.atomic
def checkout(request):
    """Process checkout and create order"""
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can checkout.')
        return redirect('ecommerce:home')

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('ecommerce:view_cart')

    # Validate stock and calculate total
    total = 0
    order_items_data = []

    for item in cart_items:
        if item.quantity > item.product.stock:
            messages.error(request, f'Not enough stock for {item.product.name}.')
            return redirect('ecommerce:view_cart')

        subtotal = item.get_subtotal()
        total += subtotal
        order_items_data.append({
            'product': item.product,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price,
            'subtotal': subtotal
        })

    # Create order
    order = Order.objects.create(
        buyer=request.user,
        total_amount=total,
        status='pending'
    )

    # Create order items and reduce stock
    for item_data in order_items_data:
        OrderItem.objects.create(
            order=order,
            product=item_data['product'],
            product_name=item_data['product_name'],
            quantity=item_data['quantity'],
            price=item_data['price']
        )
        # Reduce stock
        item_data['product'].reduce_stock(item_data['quantity'])

    # Clear cart
    cart.clear()

    # Clear session cart
    if 'cart' in request.session:
        del request.session['cart']

    # Send invoice email
    send_invoice_email(order)

    messages.success(request, 'Order placed successfully! Check your email for invoice.')
    return redirect('ecommerce:order_success', order_id=order.id)


@login_required
def order_success(request, order_id):
    """Display order confirmation"""
    order = get_object_or_404(Order, id=order_id)

    if order.buyer != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('ecommerce:home')

    return render(request, 'ecommerce/order_success.html', {'order': order})


@login_required
def order_history(request):
    """Display buyer's order history"""
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can view order history.')
        return redirect('ecommerce:home')

    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    return render(request, 'ecommerce/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """Display detailed order information"""
    order = get_object_or_404(Order, id=order_id)

    if order.buyer != request.user:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('ecommerce:home')

    return render(request, 'ecommerce/order_detail.html', {'order': order})


# Review Views
@login_required
def add_review(request, product_id):
    """Add review for a product"""
    if not request.user.groups.filter(name='Buyers').exists():
        messages.error(request, 'Only buyers can add reviews.')
        return redirect('ecommerce:product_detail', product_id=product_id)

    product = get_object_or_404(Product, id=product_id)

    # Check if user already reviewed
    if Review.objects.filter(product=product, buyer=request.user).exists():
        messages.error(request, 'You have already reviewed this product.')
        return redirect('ecommerce:product_detail', product_id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.buyer = request.user
            # is_verified will be set automatically in save() method
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('ecommerce:product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'ecommerce/review_form.html', {'form': form, 'product': product})
