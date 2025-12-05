from django.urls import path
from .views import (
    HomeView, 
    AddToCartView, 
    CartView, 
    UpdateCartView, 
    RemoveFromCartView, 
    ClearCartView,
    CheckoutView,
    OrderSuccessView,
)

app_name = 'core_ecommerce'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/remove/<int:product_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-success/<int:order_id>/', OrderSuccessView.as_view(), name='order_success'),
]