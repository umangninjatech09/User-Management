from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  
from rest_framework.permissions import IsAuthenticated
from .models import  Project, Leaves, WorkTiming
from .serializers import  ProjectSerializer, LeavesSerializer, WorkTimingSerializer, UserSignupSerializer, OTPRequestSerializer, OTPVerifySerializer, UserDetailSerializer

User = get_user_model()


# class UserListView(APIView):
#     def get(self, request):
#         users = User.objects.filter(is_deleted=False)
#         user_data = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
#         return Response(user_data)

class UserListView(APIView):
    def get(self, request):
        users = (
            User.objects
            .filter(is_deleted=False)
            .prefetch_related('projects', 'leaves_set', 'worktiming_set')  # prefetch related data efficiently
            .order_by('id')
        )

        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Request OTP
class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        otp = user.generate_otp()
        return Response({"message": "OTP sent", "otp": otp})

# Verify OTP & get JWT
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if not user.verify_otp(otp):
            return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_200_OK)



# Project Views
class ProjectListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        projects = Project.objects.filter(is_deleted=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            project = Project.objects.get(pk=pk, is_deleted=False)
        except Project.DoesNotExist:
            return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

        project.is_deleted = True
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Leaves Views

class LeavesListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request):
        leaves = Leaves.objects.filter(is_deleted=False)
        serializer = LeavesSerializer(leaves, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = LeavesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, updated_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeavesSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            leave = Leaves.objects.get(pk=pk, is_deleted=False)
        except Leaves.DoesNotExist:
            return Response({'error': 'Leave not found'}, status=status.HTTP_404_NOT_FOUND)

        leave.is_deleted = True
        leave.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# WorkTiming Views

class WorkTimingListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request):
        work_timings = WorkTiming.objects.all()
        serializer = WorkTimingSerializer(work_timings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WorkTimingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            work_timing = WorkTiming.objects.get(pk=pk)
        except WorkTiming.DoesNotExist:
            return Response({'error': 'WorkTiming not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WorkTimingSerializer(work_timing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            work_timing = WorkTiming.objects.get(pk=pk)
        except WorkTiming.DoesNotExist:
            return Response({'error': 'WorkTiming not found'}, status=status.HTTP_404_NOT_FOUND)

        work_timing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Today's Work Update :-
User Management System with Django and PostgreSQL
- Solve error in logging
- link 
'''