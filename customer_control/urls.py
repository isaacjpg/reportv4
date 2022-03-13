from django.urls import path, include
from .views import CustomerView
from rest_framework.routers import DefaultRouter

router=DefaultRouter(trailing_slash=False)

router.register('', CustomerView, 'customer')

urlpatterns = [
  path('', include(router.urls))  
]