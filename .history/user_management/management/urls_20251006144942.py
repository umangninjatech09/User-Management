from django.urls import path
from .views import  VerifyOTPView, ProjectListCreateView, LeavesListCreateView, WorkTimingListCreateView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', ProjectListCreateView.as_view(), name='project_detail'),
    path('leaves/', LeavesListCreateView.as_view(), name='leaves_list_create'),
    path('leaves/<int:pk>/', LeavesListCreateView.as_view(), name='leaves_detail'),
    path('worktiming/', WorkTimingListCreateView.as_view(), name='worktiming_list_create'),
    path('worktiming/<int:pk>/', WorkTimingListCreateView.as_view(), name='worktiming_detail'),
]
