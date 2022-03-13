from core.utils import CustomPagination, get_query
from user_control.custom_methods import  IsAuthenticatedCustom
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from user_control.views import add_user_activity
from user_control.models import CustomUser
from .serializers import EquipmentSerializer, ReportSerializer
from .models import Equipment, Report


class EquipmentView(ModelViewSet):
  queryset=Equipment.objects.all()
  serializer_class=EquipmentSerializer
  permission_classes = (IsAuthenticatedCustom,)
  pagination_class = CustomPagination

  def get_queryset(self):
    if self.request.method.lower()!='get':
      return self.queryset
    
    data = self.request.query_params.dict()
    data.pop('page', None)
    keyword=data.pop('keyword', None)
    results=self.queryset.filter(**data)
    
    if keyword:
      search_fields=('name','serial','marca','customer__name','customer__rut',)
      query=get_query(keyword, search_fields)
      return results.filter(query)
    
    return results
  
  def create(self, request, *args, **kwargs):
    request.data.update({'created_by_id':request.user.id})
    return super().create(request, *args, **kwargs)
  
  def partial_update(self, request, *args, **kwargs):
    request.data.update({'updated_by_id':request.user.id})
    return super().partial_update(request, *args, **kwargs)
  
  def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)
  
  def destroy(self, request, *args, **kwargs):
      return super().destroy(request,*args, **kwargs)

class ReportView(ModelViewSet):
  queryset=Report.objects.all()
  serializer_class=ReportSerializer
  permission_classes = (IsAuthenticatedCustom,)
  pagination_class = CustomPagination

  def get_queryset(self):
    if self.request.method.lower()!='get':
      return self.queryset
    
    data = self.request.query_params.dict()
    data.pop('page', None)
    keyword=data.pop('keyword', None)
    results=self.queryset.filter(**data)
    
    if keyword:
      search_fields=('title','equipment__name','equipment__marca','customer__name','customer__rut','created_by__name','created_by__email')
      query=get_query(keyword, search_fields)
      return results.filter(query)

    return results
  
  def create(self, request, *args, **kwargs):
    request.data.update({'created_by_id':request.user.id})
    return super().create(request, *args, **kwargs)
  
  def partial_update(self, request, *args, **kwargs):
    request.data.update({'updated_by_id':request.user.id})
    return super().partial_update(request, *args, **kwargs)
  
  def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)
  
  def destroy(self, request, *args, **kwargs):
      return super().destroy(request,*args, **kwargs)
