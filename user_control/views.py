from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.generics import  ListAPIView, GenericAPIView
from rest_framework.views import APIView
from .custom_methods import IsAuthenticatedCustom
from core.utils import get_access_token
from .serializers import (CreateUserSerializer, LoginSerializer,
 UpdatePasswordSerializer,CustomUserSerializer,UserActivitiesSerializer)
from .models import CustomUser, Roles, UserActivities
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone

def add_user_activity(user,action):
  print(user)
  UserActivities.objects.create(
    user_id=user.id,
    email=user.email,
    fullname=user.fullname,
    action=action)

class CreateUserView(GenericViewSet):
  serializer_class=CreateUserSerializer
  permission_classes=(IsAuthenticatedCustom,)

  def post(self, request, *args, **kwargs):
    valid_request=self.serializer_class(data=request.data)
    valid_request.is_valid(raise_exception=True)

    CustomUser.objects.create_user(**valid_request.validated_data)
    add_user_activity(request.user,'added new user')
    return Response({'success':'User created succesfully'},
    status=status.HTTP_201_CREATED
    )

class LoginView(GenericViewSet):
  http_methods_name=['post']
  queryset=CustomUser.objects.all()
  serializer_class=LoginSerializer

  def create(self, request, *args, **kwargs):
    valid_request=self.serializer_class(data=request.data)
    valid_request.is_valid(raise_exception=True)

    user=authenticate(**valid_request.validated_data)
    
    if not user:
      return Response({'error':'Invalid Credentials'},
      status=status.HTTP_401_UNAUTHORIZED
      )

    access=get_access_token({"user_id":user.id},1)

    user.last_login=timezone.now()
    user.save()
    add_user_activity(user,'logded in')

    return Response({'access':access})

class UpdatePasswordView(GenericViewSet):
  http_methods_name=['post']
  serializer_class=UpdatePasswordSerializer
  permission_classes=(IsAuthenticatedCustom,)

  def get_queryset(self):
      return None

  def post(self, request, *args, **kwargs):
    valid_request=self.serializer_class(data=request.data)
    valid_request.is_valid(raise_exception=True)
    
    user=authenticate(email=request.user.email,password=valid_request.validated_data['password'])
    if not user:
      raise Exception('Invalid Credentials')

    user.set_password(valid_request.validated_data['new_password'])
    user.save()
    add_user_activity(user,'updated password')
    return Response({'success':'Password updated succesfully'}, status=status.HTTP_200_OK)

class MeView(GenericViewSet):
  http_methods_name=['get']
  serializer_class=CustomUserSerializer
  permission_classes=(IsAuthenticatedCustom,)

  def list(self, request):
    return Response(self.serializer_class(request.user).data)

class UserActivitiesView(ModelViewSet):
  http_methods_name=['get']
  serializer_class=UserActivitiesSerializer
  queryset=UserActivities.objects.all()
  permission_classes=(IsAuthenticatedCustom,)

class UsersView(GenericViewSet):
  http_methods_name=['get']
  serializer_class=CustomUserSerializer
  queryset=CustomUser.objects.all()
  permission_classes=(IsAuthenticatedCustom,)    

  def list(self, request):
    users=self.queryset.filter(is_superuser=False)
    data=self.serializer_class(users,many=True).data
    return Response(data)
