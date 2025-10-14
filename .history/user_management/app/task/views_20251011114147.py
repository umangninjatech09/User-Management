from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer
