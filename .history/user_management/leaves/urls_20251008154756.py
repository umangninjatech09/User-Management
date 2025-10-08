from django.urls import path
from .views import LeavesListCreateView, WorkTimingListCreateView, UserSignupView, RequestOTPView, UserListView
from rest_framework_simplejwt.views import TokenRefreshView