from django.db import models
from customer_control.models import Address, Contact, Customer
from user_control.views import add_user_activity
from user_control.models import CustomUser

class Equipment(models.Model):
  serial=models.CharField(max_length=12,unique=True)
  name=models.CharField(max_length=255)
  marca=models.CharField(max_length=255)
  customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True, related_name='equipments')
  address=models.ForeignKey(Address, on_delete=models.SET_NULL,null=True, related_name='equipments')
  created_by=models.ForeignKey('user_control.CustomUser',on_delete=models.SET_NULL,null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  class Meta:
    ordering=('name',)

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.old_name=self.name
    self.old_serial=self.serial
  
  def save(self, *args, **kwargs):
    action=f'added new equipment {self.serial} {self.name}'
    created_by=self.created_by

    #Revisa si es una actualizacion o nuevo equipo
    if self.pk is not None:
      action=f'updated equipment from "{self.old_name} to {self.name}" -- "from {self.old_serial} to {self.serial}'
    
    self.serial = self.serial.upper() #Lleva el RUT a mayusculas
    self.serial=self.serial.replace(" ", "")
    self.name=self.name.strip()
    self.name=self.name.upper()
    super().save(*args, **kwargs)
    add_user_activity(created_by, action=action)
  
  def delete(self, *args, **kwargs):
    action=f'deleted equipment {self.serial} {self.name}'
    created_by=self.created_by
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return f'{self.serial} {self.name}'

class Report(models.Model):
  equipment=models.ForeignKey(Equipment, on_delete=models.SET_NULL,null=True, related_name='reports')
  customer=models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True, related_name='reports')
  contact=models.ForeignKey(Contact,on_delete=models.SET_NULL,null=True,related_name='reports')
  created_by=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True, related_name='reports')
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)
  date=models.DateField(blank=True,null=True)
  title=models.CharField(max_length=255)
  report=models.TextField(blank=True,null=True)
  recomendations=models.TextField(blank=True,null=True)
  service_hours=models.IntegerField(default=0)
  parts=models.JSONField(default=list)

  def save(self, *args, **kwargs):
    action=f'added new report for equipment {self.customer.name} {self.equipment.serial} {self.equipment.name} {self.title} {self.date} '
    created_by=self.created_by
    #Revisa si es una actualizacion o nuevo equipo
    if self.pk is not None:
      action=f'updated report "{self.customer.name} {self.equipment.serial} {self.equipment.name} {self.title} {self.date}'
    super().save(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def delete(self, *args, **kwargs):
    action=f'deleted report {self.customer.name} {self.equipment.serial} {self.equipment.name} {self.title} {self.date}'
    created_by=self.created_by
    super().delete(*args, **kwargs)
    add_user_activity(created_by, action=action)

  def __str__(self):
    return f'{self.customer.name} {self.date} {self.equipment.serial} {self.equipment.name}'