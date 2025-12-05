from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from product.models import Product, Category, ProductReview
from product.forms import CategoryForm, ReviewForm
from core_ecommerce.models import Order, OrderItem


class ProductDetailView(View):
    template_name = 'product/detail.html'

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        # Get related products from the same category
        related_products = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:4]
        
        # Get reviews for this product
        reviews = ProductReview.objects.filter(product=product).select_related('user').order_by('-created_at')
        
        # Calculate average rating
        rating_stats = reviews.aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )
        # Convert avg_rating to int for star display
        if rating_stats['avg_rating']:
            rating_stats['avg_rating_int'] = int(round(rating_stats['avg_rating']))
        else:
            rating_stats['avg_rating_int'] = 0
        
        # Check if user has purchased this product (for review eligibility)
        can_review = False
        user_review = None
        has_purchased = False
        
        if request.user.is_authenticated and not request.user.is_vendor:
            # Check if user has purchased this product
            has_purchased = OrderItem.objects.filter(
                order__customer=request.user,
                product=product,
                order__status__in=['pending', 'processing', 'shipped', 'delivered']
            ).exists()
            
            # Check if user already has a review
            try:
                user_review = ProductReview.objects.get(product=product, user=request.user)
            except ProductReview.DoesNotExist:
                user_review = None
            
            # Can review if purchased and hasn't reviewed yet
            can_review = has_purchased and user_review is None
        
        # Paginate reviews
        paginator = Paginator(reviews, 5)  # 5 reviews per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'product': product,
            'related_products': related_products,
            'reviews': page_obj,
            'rating_stats': rating_stats,
            'can_review': can_review,
            'has_purchased': has_purchased,
            'user_review': user_review,
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


@method_decorator(login_required, name='dispatch')
class AddReviewView(View):
    """Add a review for a product"""
    
    def post(self, request, product_id):
        # Only buyers can leave reviews
        if request.user.is_vendor:
            messages.error(request, 'Vendors cannot leave reviews.')
            return redirect('core_ecommerce:home')
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user has purchased this product
        has_purchased = OrderItem.objects.filter(
            order__customer=request.user,
            product=product,
            order__status__in=['pending', 'processing', 'shipped', 'delivered']
        ).exists()
        
        if not has_purchased:
            messages.error(request, 'You can only review products you have purchased.')
            return redirect('product:product_detail', slug=product.slug)
        
        # Check if user already has a review
        existing_review = ProductReview.objects.filter(product=product, user=request.user).first()
        if existing_review:
            messages.info(request, 'You have already reviewed this product. You can edit your review instead.')
            return redirect('product:edit_review', review_id=existing_review.id)
        
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product:product_detail', slug=product.slug)
        else:
            messages.error(request, 'Please correct the errors in your review.')
            return redirect('product:product_detail', slug=product.slug)


@method_decorator(login_required, name='dispatch')
class EditReviewView(View):
    """Edit an existing review"""
    template_name = 'product/review_form.html'
    
    def get(self, request, review_id):
        review = get_object_or_404(ProductReview, id=review_id)
        
        # Only the review owner can edit
        if review.user != request.user:
            messages.error(request, 'You can only edit your own reviews.')
            return redirect('product:product_detail', slug=review.product.slug)
        
        form = ReviewForm(instance=review)
        context = {
            'form': form,
            'review': review,
            'product': review.product,
            'is_edit': True,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, review_id):
        review = get_object_or_404(ProductReview, id=review_id)
        
        # Only the review owner can edit
        if review.user != request.user:
            messages.error(request, 'You can only edit your own reviews.')
            return redirect('product:product_detail', slug=review.product.slug)
        
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('product:product_detail', slug=review.product.slug)
        
        context = {
            'form': form,
            'review': review,
            'product': review.product,
            'is_edit': True,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class DeleteReviewView(View):
    """Delete a review"""
    
    def post(self, request, review_id):
        review = get_object_or_404(ProductReview, id=review_id)
        product_slug = review.product.slug
        
        # Only the review owner can delete
        if review.user != request.user:
            messages.error(request, 'You can only delete your own reviews.')
            return redirect('product:product_detail', slug=product_slug)
        
        review.delete()
        messages.success(request, 'Your review has been deleted successfully!')
        return redirect('product:product_detail', slug=product_slug)
