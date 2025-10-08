from django.urls import path
from .views import  VerifyOTPView, ProjectListCreateView, LeavesListCreateView, WorkTimingListCreateView, UserSignupView, RequestOTPView, UserListView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
   
    path('users/', UserListView.as_view(), name='user_list'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('login/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', ProjectListCreateView.as_view(), name='project_detail'),
    path('leaves/', LeavesListCreateView.as_view(), name='leaves_list_create'),
    path('leaves/<int:pk>/', LeavesListCreateView.as_view(), name='leaves_detail'),
    path('worktiming/', WorkTimingListCreateView.as_view(), name='worktiming_list_create'),
    path('worktiming/<int:pk>/', WorkTimingListCreateView.as_view(), name='worktiming_detail'),
   
]
