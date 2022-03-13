from django.urls import path, include
from .views import EquipmentView, ReportView
from rest_framework.routers import DefaultRouter

router=DefaultRouter(trailing_slash=False)

router.register('machines', EquipmentView, 'equipment')
router.register('report', ReportView, 'report')

urlpatterns = [
  path('', include(router.urls))  
]