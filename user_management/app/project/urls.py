from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('project/', ProjectDetailView.as_view(), name='user_projects'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),

]