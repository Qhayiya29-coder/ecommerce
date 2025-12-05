from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from product.models import Product, Category
from product.forms import CategoryForm


class ProductDetailView(View):
    template_name = 'product/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        # Get related products from the same category
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CategoryListView(View):
    """List all categories"""
    template_name = 'product/category_list.html'
    
    def get(self, request):
        categories = Category.objects.all().order_by('name')
        
        # Pagination
        paginator = Paginator(categories, 20)  # Show 20 categories per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'categories': page_obj,
            'is_vendor': request.user.is_vendor,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(View):
    """Create a new category"""
    template_name = 'product/category_form.html'
    
    def get(self, request):
        # Only vendors can create categories
        if not request.user.is_vendor:
            messages.error(request, 'Only vendors can create categories.')
            return redirect('core_ecommerce:home')
        
        form = CategoryForm()
        context = {
            'form': form,
            'is_edit': False,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        # Only vendors can create categories
        if not request.user.is_vendor:
            messages.error(request, 'Only vendors can create categories.')
            return redirect('core_ecommerce:home')
        
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" created successfully!')
            return redirect('product:category_list')
        
        context = {
            'form': form,
            'is_edit': False,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CategoryEditView(View):
    """Edit an existing category"""
    template_name = 'product/category_form.html'
    
    def get(self, request, pk):
        # Only vendors can edit categories
        if not request.user.is_vendor:
            messages.error(request, 'Only vendors can edit categories.')
            return redirect('core_ecommerce:home')
        
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        context = {
            'form': form,
            'category': category,
            'is_edit': True,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        # Only vendors can edit categories
        if not request.user.is_vendor:
            messages.error(request, 'Only vendors can edit categories.')
            return redirect('core_ecommerce:home')
        
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('product:category_list')
        
        context = {
            'form': form,
            'category': category,
            'is_edit': True,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(View):
    """Delete a category"""
    
    def post(self, request, pk):
        # Only vendors can delete categories
        if not request.user.is_vendor:
            messages.error(request, 'Only vendors can delete categories.')
            return redirect('core_ecommerce:home')
        
        category = get_object_or_404(Category, pk=pk)
        category_name = category.name
        
        # Check if category has products
        product_count = Product.objects.filter(category=category).count()
        if product_count > 0:
            messages.error(
                request, 
                f'Cannot delete category "{category_name}" because it has {product_count} product(s). '
                'Please remove or reassign products first.'
            )
            return redirect('product:category_list')
        
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('product:category_list')
