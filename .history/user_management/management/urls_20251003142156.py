from django.urls import path
from .views import RegisterView, VerifyOTPView

urlpatterns = [
    path('/register/', RegisterView.as_view(), name='register'),
    path('/verify/', VerifyOTPView.as_view(), name='verify'),
]
