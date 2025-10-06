from django.urls import path
from .views import  VerifyOTPView, ProjectListCreateView, LeavesListCreateView, WorkTimingListCreateView, UserSignupView, RequestOTPView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('verify/', VerifyOTPView.as_view(), name='verify'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('reset-password/', SimpleResetPasswordView.as_view(), name='reset_password'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('profile/', ProfileListCreateView.as_view(), name='profile_list_create'),
    # path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', ProjectListCreateView.as_view(), name='project_detail'),
    path('leaves/', LeavesListCreateView.as_view(), name='leaves_list_create'),
    path('leaves/<int:pk>/', LeavesListCreateView.as_view(), name='leaves_detail'),
    path('worktiming/', WorkTimingListCreateView.as_view(), name='worktiming_list_create'),
    path('worktiming/<int:pk>/', WorkTimingListCreateView.as_view(), name='worktiming_detail'),


    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('login/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
