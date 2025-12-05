from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class UserTypeForm(forms.Form):
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-radio accent-blue-500'}),  # Added Tailwind class
        required=True)


