from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # or your custom User model

User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
            otp=otp
        )

        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            'no-reply@example.com',
            [email],
        )

        return Response({'message': 'User registered. OTP sent to email.'}, status=201)


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP required'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if user.is_verified:
            return Response({'message': 'User already activated.'})

        if user.otp == otp:
            user.is_active = True
            user.is_verified = True
            user.otp = ''
            user.save()

            return Response({'message': 'OTP verified. Account activated.'})
        else:
            return Response({'error': 'Invalid OTP'}, status=400)



class SimpleResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not email or not new_password:
            return Response({'error': 'Email and new password are required'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful.'})



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=400)

        # Lookup user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=401)

        # Authenticate using username and password
        user = authenticate(request, username=user_obj.username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        if not user.is_active or not getattr(user, 'is_verified', True):
            return Response({'error': 'Account is not activated.'}, status=403)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
