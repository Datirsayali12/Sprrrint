from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse

# Generate Token Manually
class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]

  def post(self, request, format=None):
    data = request.data
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    password2 = data.get('password2')

    if not (email and name and password and password2):
      return JsonResponse({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
      return JsonResponse({'error': 'Password and Confirm Password do not match'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
      return JsonResponse({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(email=email, name=name, password=password)
    token = self.get_tokens_for_user(user)
    return JsonResponse({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)

  def get_tokens_for_user(self, user):
    refresh = RefreshToken.for_user(user)
    return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
    }
