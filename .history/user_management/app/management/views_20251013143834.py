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
from .models import WorkTiming
from app.project.models import Project
from app.leaves.models import Leaves
from .serializers import  WorkTimingSerializer, UserSignupSerializer, OTPVerifySerializer, UserDetailSerializer
from django.utils import timezone

User = get_user_model()

class UsersListView(APIView):
    def get(self, request):
        users = (
            User.objects
            .filter(is_deleted=False)
            .prefetch_related('projects', 'leaves_set', 'worktiming_set') 
            .order_by('id')
        )
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = (
            User.objects
            .filter(id=request.user.id, is_deleted=False)
            .prefetch_related('projects', 'leaves_set', 'worktiming_set')
            .first()
        )

        if not user:
            return Response({"detail": "User not found."}, status=404)

        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_deleted=False)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSignupSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_deleted=False)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_deleted = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

        if user.last_token_issued_at and (timezone.now() - user.last_token_issued_at).seconds < 10:
            return Response({"error": "Token already issued for this OTP"}, status=400)

        refresh = RefreshToken.for_user(user)
        user.last_token_issued_at = timezone.now()
        user.save()

        return Response({
            "message": "OTP verified",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)


# WorkTiming Views

class WorkTimingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        work_timings = WorkTiming.objects.filter(user=user, is_deleted=False)

        if not work_timings.exists():
            return Response(
                {'message': 'No work timings found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = WorkTimingSerializer(work_timings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        authenticated_user = request.user
        serializer = WorkTimingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=authenticated_user, created_by=authenticated_user, updated_by=authenticated_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
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