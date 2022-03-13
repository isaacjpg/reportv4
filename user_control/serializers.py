from rest_framework import serializers
from .models import CustomUser, Roles, UserActivities

class CreateUserSerializer(serializers.Serializer):
  email=serializers.EmailField()
  password=serializers.CharField(min_length=8)
  fullname=serializers.CharField(max_length=255)
  role=serializers.ChoiceField(choices=Roles)

class LoginSerializer(serializers.Serializer):
  email=serializers.EmailField()
  password=serializers.CharField()

class UpdatePasswordSerializer(serializers.Serializer):
  password=serializers.CharField()
  new_password=serializers.CharField(min_length=8)
  

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model=CustomUser
    exclude=('password',)

class UserActivitiesSerializer(serializers.ModelSerializer):
  class Meta:
    model=UserActivities
    fields=('__all__')