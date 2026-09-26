from .views import RegisterView
from .views import LoginView
from .views import UsernameValidationView
from .views import EmailValidationView
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from .views import CustomLogoutView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('validate-username/', UsernameValidationView.as_view(), name='validate-username'),
    path('validate-email/', EmailValidationView.as_view(), name='validate-email'),
    path('reset-password/', CustomPasswordResetView.as_view(), name='reset-password'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/', CustomLogoutView.as_view(), name='logout')
]
