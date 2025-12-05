from django.shortcuts import render, redirect
from django.views.generic import FormView, View

from accounts.forms import UserTypeForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from customer.forms import CustomerUserCreationForm
from vendor.forms import VendorUserCreationForm
from django.contrib.auth import login, logout



class GetUserType(View):
    form_class = UserTypeForm
    template_name = 'accounts/user_type.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self.request.session['user_type'] = form.cleaned_data['user_type']
            return redirect('accounts:register')
        return render(request, self.template_name, {'form': form})


class RegistrationView(FormView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def dispatch(self, request, *args, **kwargs):
        # Force user to pick a type first
        if not request.session.get('user_type'):
            return redirect('accounts:user_type')
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        # Return the appropriate form based on user type
        user_type = self.request.session.get('user_type', 'customer')
        if user_type == 'vendor':
            return VendorUserCreationForm
        return CustomerUserCreationForm

    def form_valid(self, form):
        user = form.save()
        # Set user type from session
        user.user_type = self.request.session.get('user_type', 'customer')
        user.save()
        # Clear user type from session after successful registration
        self.request.session.pop('user_type', None)
        return super().form_valid(form) 

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('core_ecommerce:home')
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        
        # Redirect based on user type
        if user.is_vendor:
            return redirect('vendor:vendor_dashboard')
        else:
            return redirect('core_ecommerce:home')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('core_ecommerce:home')