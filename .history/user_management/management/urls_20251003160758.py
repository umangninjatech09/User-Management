from django.urls import path
from .views import RegisterView, VerifyOTPView, SimpleResetPasswordView, LoginView, p
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyOTPView.as_view(), name='verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', SimpleResetPasswordView.as_view(), name='reset_password'),
    path('login/', LoginView.as_view(), name='login'),
]
