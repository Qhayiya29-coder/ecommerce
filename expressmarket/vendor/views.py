from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Count, Sum
from django.core.paginator import Paginator

from vendor.models import Vendor, Store
from vendor.forms import StoreForm, ProductForm
from product.models import Product, Category
from core_ecommerce.models import OrderItem


def vendor_required(view_func):
    """Decorator to check if user is a vendor"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this page.')
            return redirect('accounts:login')
        if not request.user.is_vendor:
            messages.error(request, 'You must be a vendor to access this page.')
            return redirect('core_ecommerce:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class VendorDashboardView(View):
    """Main vendor dashboard"""
    template_name = 'vendor/dashboard.html'
    
    def get(self, request):
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found. Please complete your vendor registration.')
            return redirect('accounts:register')
        
        store = None
        try:
            store = Store.objects.get(owner=request.user)
        except Store.DoesNotExist:
            pass
        
        # Get vendor's products
        products = Product.objects.filter(vendor=vendor).select_related('category')
        
        # Get order statistics
        order_items = OrderItem.objects.filter(product__vendor=vendor).select_related('order', 'product')
        total_orders = order_items.values('order').distinct().count()
        total_sales = order_items.aggregate(total=Sum('subtotal'))['total'] or 0
        total_products_sold = order_items.aggregate(total=Sum('quantity'))['total'] or 0
        
        # Recent orders
        recent_orders = order_items.select_related('order', 'product').order_by('-order__created_at')[:5]
        
        context = {
            'vendor': vendor,
            'store': store,
            'products': products[:5],  # Show latest 5 products
            'total_products': products.count(),
            'total_orders': total_orders,
            'total_sales': total_sales,
            'total_products_sold': total_products_sold,
            'recent_orders': recent_orders,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class StoreCreateView(View):
    """Create or edit store"""
    template_name = 'vendor/store_form.html'
    
    def get(self, request):
        store = None
        try:
            store = Store.objects.get(owner=request.user)
            form = StoreForm(instance=store)
            is_edit = True
        except Store.DoesNotExist:
            form = StoreForm()
            is_edit = False
        
        context = {
            'form': form,
            'is_edit': is_edit,
            'store': store,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        store = None
        is_edit = False
        try:
            store = Store.objects.get(owner=request.user)
            form = StoreForm(request.POST, instance=store)
            is_edit = True
        except Store.DoesNotExist:
            form = StoreForm(request.POST)
            is_edit = False
        
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            
            if is_edit:
                messages.success(request, 'Store updated successfully!')
            else:
                messages.success(request, 'Store created successfully!')
            return redirect('vendor:vendor_dashboard')
        
        context = {
            'form': form,
            'is_edit': is_edit,
            'store': store,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class ProductListView(View):
    """List all vendor products"""
    template_name = 'vendor/product_list.html'
    
    def get(self, request):
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found.')
            return redirect('vendor:vendor_dashboard')
        
        products = Product.objects.filter(vendor=vendor).select_related('category').order_by('-created_at')
        
        # Pagination
        paginator = Paginator(products, 12)
        page = request.GET.get('page', 1)
        try:
            products_page = paginator.page(page)
        except:
            products_page = paginator.page(1)
        
        context = {
            'products': products_page,
            'vendor': vendor,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class ProductCreateView(View):
    """Create a new product"""
    template_name = 'vendor/product_form.html'
    
    def get(self, request):
        form = ProductForm()
        context = {
            'form': form,
            'is_edit': False,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        try:
            vendor = Vendor.objects.get(user=request.user)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found.')
            return redirect('vendor:vendor_dashboard')
        
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = vendor
            product.save()
            messages.success(request, f'Product "{product.name}" created successfully!')
            return redirect('vendor:product_list')
        
        context = {
            'form': form,
            'is_edit': False,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class ProductEditView(View):
    """Edit an existing product"""
    template_name = 'vendor/product_form.html'
    
    def get(self, request, product_id):
        try:
            vendor = Vendor.objects.get(user=request.user)
            product = get_object_or_404(Product, id=product_id, vendor=vendor)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found.')
            return redirect('vendor:vendor_dashboard')
        
        form = ProductForm(instance=product)
        context = {
            'form': form,
            'product': product,
            'is_edit': True,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, product_id):
        try:
            vendor = Vendor.objects.get(user=request.user)
            product = get_object_or_404(Product, id=product_id, vendor=vendor)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found.')
            return redirect('vendor:vendor_dashboard')
        
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('vendor:product_list')
        
        context = {
            'form': form,
            'product': product,
            'is_edit': True,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
@method_decorator(vendor_required, name='dispatch')
class ProductDeleteView(View):
    """Delete a product"""
    
    def post(self, request, product_id):
        try:
            vendor = Vendor.objects.get(user=request.user)
            product = get_object_or_404(Product, id=product_id, vendor=vendor)
        except Vendor.DoesNotExist:
            messages.error(request, 'Vendor profile not found.')
            return redirect('vendor:vendor_dashboard')
        
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('vendor:product_list')
