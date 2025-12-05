from django.shortcuts import render, get_object_or_404
from django.views import View
from product.models import Product, Category


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
