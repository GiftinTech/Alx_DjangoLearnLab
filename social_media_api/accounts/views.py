from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
  serializer_class = RegisterSerializer
  permission_classes = [permissions.AllowAny]

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.get(user=user)
    return Response({
      'user': serializer.data,
      'token': token.key
    }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
  serializer_class = LoginSerializer
  permission_classes = [permissions.AllowAny]

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
      username=serializer.validated_data['username'],
      password=serializer.validated_data['password']
    )
    if user:
      token, created = Token.objects.get_or_create(user=user)
      return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
  user_to_follow = get_object_or_404(CustomUser, id=user_id)
  request.user.following.add(user_to_follow)
  return Response({
    "message": f"You are now following {user_to_follow.username}",
    "user": UserSerializer(user_to_follow).data
  })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
  user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
  request.user.following.remove(user_to_unfollow)
  return Response({
    "message": f"You have unfollowed {user_to_unfollow.username}",
    "user": UserSerializer(user_to_unfollow).data
  })
