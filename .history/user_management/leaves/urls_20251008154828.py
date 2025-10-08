from django.urls import path
from .views import LeavesListCreateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('leaves/', LeavesListCreateView.as_view(), name='leaves_list_create'),
    path('leaves/<int:pk>/', LeavesListCreateView.as_view(), name='leaves_detail'),
