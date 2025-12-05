from django.views.generic import FormView
from customer.forms import CustomerUserCreationForm

class CustomerRegistrationView(CreateView):
    model = Customer
    form_class = CustomerUserCreationForm
    template_name = 'customer/registration.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)