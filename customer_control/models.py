import re
from django.db import models
from user_control.views import add_user_activity
from user_control.models import UserActivities, CustomUser

class Customer(models.Model):
  rut=models.CharField(max_length=12,unique=True)
  name=models.CharField(max_length=255,unique=True)
  created_by=models.ForeignKey('user_control.CustomUser',on_delete=models.SET_NULL,null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    ordering=('name',)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.old_name=self.name
    self.old_rut=self.rut
  
  def save(self, *args, **kwargs):
    action=f'added new customer {self.rut} {self.name}'
    created_by=self.created_by

    #Revisa si es una actualizacion o nuevo cliente
    if self.pk is not None:
      action=f'updated customer from "{self.old_name} to {self.name}" -- "from {self.old_rut} to {self.rut}'
    
    self.rut = self.rut.upper() #Lleva el RUT a mayusculas
    self.rut=self.rut.replace(" ", "") #Elimina espacios en blanco
    self.name=self.name.strip() #Elimina espacios en blanco al inicio y final de la cadena
    self.name=self.name.upper()
    super().save(*args, **kwargs)
    add_user_activity(created_by, action=action)
  
  def delete(self, *args, **kwargs):
    action=f'deleted customer {self.rut} {self.name}'
    created_by=self.created_by
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return f'{self.rut} {self.name}'

class Contact(models.Model):
  customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='contacts')
  fullname=models.CharField(max_length=255)
  phone=models.CharField(max_length=255)
  email=models.EmailField()

  def save(self, *args, **kwargs):
    self.fullname=self.fullname.strip()
    self.fullname=self.fullname.capitalize()
    self.phone=self.phone.strip()
    super().save(*args, **kwargs)

class Address(models.Model):
  customer=models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses')
  street=models.CharField(max_length=255)
  number=models.CharField(max_length=255)
  region=models.CharField(max_length=255)
  comune=models.CharField(max_length=255)

  def save(self, *args, **kwargs):
    self.street=self.street.strip()
    self.street=self.street.capitalize()
    self.number=self.number.strip()
    self.region=self.region.strip()
    self.region=self.region.capitalize()
    self.comune=self.comune.strip()
    self.comune=self.comune.capitalize()
    super().save(*args, **kwargs)

