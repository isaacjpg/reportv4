from rest_framework import serializers

from customer_control.serializers import AddressSerializer, ContactSerializer, CustomerSerializer
from .models import Equipment, Report
from user_control.serializers import CustomUserSerializer, CustomUser

class EquipmentSerializer(serializers.ModelSerializer):
  created_by=CustomUserSerializer(read_only=True)
  created_by_id=serializers.CharField(write_only=True,required=False)
  updated_by=CustomUserSerializer(read_only=True)
  updated_by_id=serializers.CharField(write_only=True,required=False)
  customer_id=serializers.CharField(write_only=True)
  customer=CustomerSerializer(read_only=True)
  address_id=serializers.CharField(write_only=True)
  address=AddressSerializer(read_only=True)
  class Meta:
    model = Equipment
    fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
  created_by=CustomUserSerializer(read_only=True)
  created_by_id=serializers.CharField(write_only=True,required=False)
  updated_by=CustomUserSerializer(read_only=True)
  updated_by_id=serializers.CharField(write_only=True,required=False)
  equipment_id=serializers.CharField(write_only=True)
  equipment=EquipmentSerializer(read_only=True)
  customer_id=serializers.CharField(write_only=True)
  customer=CustomerSerializer(read_only=True)
  contact_id=serializers.CharField(write_only=True)
  contact=ContactSerializer(read_only=True)
  class Meta:
    model = Report
    fields = '__all__'