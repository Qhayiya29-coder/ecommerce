from django.urls import path
from .views import (
    ProductDetailView,
    CategoryListView,
    CategoryCreateView,
    CategoryEditView,
    CategoryDeleteView,
)

app_name = 'product'
urlpatterns = [
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryEditView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]

