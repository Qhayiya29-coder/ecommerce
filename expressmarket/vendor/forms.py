from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from vendor.models import Vendor, Store
from product.models import Product, Category


class VendorUserCreationForm(UserCreationForm):
    business_name = forms.CharField(max_length=150, required=True, label="Business Name")
    tin = forms.CharField(max_length=100, required=True, label="TIN")
    logo = forms.ImageField(required=False, label="Logo (optional)")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "business_name",
            "tin",
            "logo",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'vendor'  # Set user_type instead of is_vendor (which is a read-only property)
        if commit:
            user.save()
            Vendor.objects.create(
                user=user,
                business_name=self.cleaned_data["business_name"],
                tin=self.cleaned_data["tin"],
                logo=self.cleaned_data.get("logo"),
                rating=1,  # Default rating for new vendors
            )
        return user


class StoreForm(forms.ModelForm):
    """Form for creating/editing a store"""
    
    class Meta:
        model = Store
        fields = ['store_name', 'description', 'address', 'region', 'city']
        widgets = {
            'store_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Store Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Store Description',
                'rows': 4
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Street Address'
            }),
            'region': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Region/State'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'City'
            }),
        }


class ProductForm(forms.ModelForm):
    """Form for creating/editing a product"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Product Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Product Description',
                'rows': 5
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make image optional when editing
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
