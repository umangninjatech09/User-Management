from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Task
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
