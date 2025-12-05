from django.urls import path
from .views import (
    ProductDetailView,
    CategoryListView,
    CategoryCreateView,
    CategoryEditView,
    CategoryDeleteView,
    AddReviewView,
    EditReviewView,
    DeleteReviewView,
)

app_name = 'product'
urlpatterns = [
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', CategoryEditView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('product/<int:product_id>/review/add/', AddReviewView.as_view(), name='add_review'),
    path('review/<int:review_id>/edit/', EditReviewView.as_view(), name='edit_review'),
    path('review/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete_review'),
]

