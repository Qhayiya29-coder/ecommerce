from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from customer.models import Customer

class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True, help_text="Your contact phone number")
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Your shipping address (optional)"
    )
    billing_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Your billing address (optional)"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_type = 'customer'
        if commit:
            user.save()
            # Create Customer profile if it doesn't exist
            Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data["phone"],
                    'shipping_address': self.cleaned_data.get("shipping_address", ""),
                    'billing_address': self.cleaned_data.get("billing_address", "")
                }
            )
        return user