from django.urls import path
from .views import  VerifyOTPView, WorkTimingListCreateView, UserSignupView, RequestOTPView, UserListView, UserUpdateView, UserDeleteView, us


urlpatterns = [
    path('users/', UsersListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/request-otp/', RequestOTPView.as_view(), name='request-otp'),
    path('login/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('worktiming/', WorkTimingListCreateView.as_view(), name='worktiming_list_create'),
    path('worktiming/<int:pk>/', WorkTimingListCreateView.as_view(), name='worktiming_detail'),
]