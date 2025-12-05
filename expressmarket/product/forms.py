from django import forms
from .models import Category, ProductReview


class CategoryForm(forms.ModelForm):
    """Form for creating/editing a category"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Category Description (optional)',
                'rows': 4
            }),
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            name = name.strip()
            # Check for duplicate name (excluding current instance if editing)
            qs = Category.objects.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('A category with this name already exists.')
        return name


class ReviewForm(forms.ModelForm):
    """Form for creating/editing product reviews"""
    
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'min': 1,
                'max': 5,
                'placeholder': 'Rating (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Write your review...',
                'rows': 5
            }),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating and (rating < 1 or rating > 5):
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating

