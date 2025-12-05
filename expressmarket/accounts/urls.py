from django.urls import path
from .views import GetUserType, LoginView, LogoutView, RegistrationView



app_name = 'accounts'
urlpatterns = [
    path('get-user-type/', GetUserType.as_view(), name='user_type'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('register/', RegistrationView.as_view(), name='register'),
]