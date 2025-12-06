from django.urls import path
from . import views

app_name = 'ecommerce'

urlpatterns = [
    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Password Reset
    path('password-reset/', views.request_password_reset, name='request_password_reset'),
    path('reset-password/<str:token>/', views.reset_user_password, name='reset_password'),

    # Home and Browse
    path('', views.home, name='home'),
    path('browse/', views.browse_products, name='browse_products'),

    # Vendor Store Management
    path('stores/create/', views.create_store, name='create_store'),
    path('stores/my-stores/', views.my_stores, name='my_stores'),
    path('stores/<int:store_id>/edit/', views.edit_store, name='edit_store'),
    path('stores/<int:store_id>/delete/', views.delete_store, name='delete_store'),

    # Vendor Product Management
    path('stores/<int:store_id>/products/', views.store_products, name='store_products'),
    path('stores/<int:store_id>/products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),

    # Buyer Product Views
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),

    # Cart Management
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Reviews
    path('products/<int:product_id>/review/', views.add_review, name='add_review'),
]

