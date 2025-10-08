from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project_list_create'),
    path('projects/<int:pk>/', ProjectListCreateView.as_view(), name='project_detail'),
]