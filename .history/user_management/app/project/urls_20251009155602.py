from django.urls import path
from .views import ProjectListCreateView,
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', ProjectListCreateView.as_view(), name='project_detail'),
]