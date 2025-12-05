from django.urls import path
from .views import (
    VendorDashboardView,
    StoreCreateView,
    ProductListView,
    ProductCreateView,
    ProductEditView,
    ProductDeleteView,
)

app_name = 'vendor'
urlpatterns = [
    path('dashboard/', VendorDashboardView.as_view(), name='vendor_dashboard'),
    path('store/create/', StoreCreateView.as_view(), name='store_create'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:product_id>/edit/', ProductEditView.as_view(), name='product_edit'),
    path('products/<int:product_id>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]

