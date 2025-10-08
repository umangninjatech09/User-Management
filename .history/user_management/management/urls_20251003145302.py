from django.urls import path
from .views import RegisterView, VerifyOTPView,
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyOTPView.as_view(), name='verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend_otp'),  # <-- add this

]
