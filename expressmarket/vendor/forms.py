from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User
from vendor.models import Vendor


class VendorUserCreationForm(UserCreationForm):
    business_name = forms.CharField(max_length=150, required=True, label="Business Name")
    tin = forms.CharField(max_length=100, required=True, label="TIN")
    logo = forms.ImageField(required=False, label="Logo (optional)")
    rating = forms.IntegerField(min_value=1, max_value=5, required=False, initial=3, label="Rating (1-5)")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "business_name",
            "tin",
            "logo",
            "rating",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vendor = True
        user.user_type = 'vendor'
        if commit:
            user.save()
            Vendor.objects.create(
                user=user,
                business_name=self.cleaned_data["business_name"],
                tin=self.cleaned_data["tin"],
                logo=self.cleaned_data.get("logo"),
                rating=self.cleaned_data.get("rating") or 1,
            )
        return user
