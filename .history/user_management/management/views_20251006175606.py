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
from .serializers import  ProjectSerializer, LeavesSerializer, WorkTimingSerializer, UserSignupSerializer, OTPRequestSerializer, OTPVerifySerializer

User = get_user_model()




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





# def generate_otp():
#     return str(random.randint(100000, 999999))

# class RegisterView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not all([username, email, password]):
#             return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

#         otp = generate_otp()

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password,
#             is_active=False,
#             otp=otp
#         )

#         send_mail(
#             'Your OTP Code',
#             f'Your OTP is: {otp}',
#             'no-reply@example.com',
#             [email],
#         )

#         return Response({'message': 'User registered. OTP sent to email.'}, status=201)


# class VerifyOTPView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         otp = request.data.get('otp')

#         if not email or not otp:
#             return Response({'error': 'Email and OTP required'}, status=400)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=404)

#         if user.is_verified:
#             return Response({'message': 'User already activated.'})

#         if user.otp == otp:
#             user.is_active = True
#             user.is_verified = True
#             user.otp = ''
#             user.save()

#             return Response({'message': 'OTP verified. Account activated.'})
#         else:
#             return Response({'error': 'Invalid OTP'}, status=400)



# class SimpleResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         new_password = request.data.get('new_password')

#         if not email or not new_password:
#             return Response({'error': 'Email and new password are required'}, status=400)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=404)

#         user.set_password(new_password)
#         user.save()

#         return Response({'message': 'Password reset successful.'})



# class LoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({'error': 'Email and password are required'}, status=400)

#         # Lookup user by email
#         try:
#             user_obj = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return Response({'error': 'Invalid credentials'}, status=401)

#         # Authenticate using username and password
#         user = authenticate(request, username=user_obj.username, password=password)
#         if user is None:
#             return Response({'error': 'Invalid credentials'}, status=401)

#         if not user.is_active or not getattr(user, 'is_verified', True):
#             return Response({'error': 'Account is not activated.'}, status=403)

#         # Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'access': str(refresh.access_token),
#             'refresh': str(refresh),
#         })


# # Profile Views
# class ProfileListCreateView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]

#     def get(self, request):
#         profiles = Profile.get_active()
#         serializer = ProfileSerializer(profiles, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProfileSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProfileDetailView(APIView):
#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [AllowAny()]
#         return [IsAuthenticated()]
    
#     def get_object(self, pk):
#         try:
#             return Profile.objects.get(pk=pk, is_deleted=False)
#         except Profile.DoesNotExist:
#             return None
        
#     def get(self, request, pk):
#         profile = self.get_object(pk)
#         if not profile:
#             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProfileSerializer(profile)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         profile = self.get_object(pk)
#         if not profile:
#             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         profile = self.get_object(pk)
#         if not profile:
#             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = ProfileSerializer(profile, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         profile = self.get_object(pk)
#         if not profile:
#             return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
#         profile.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    


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