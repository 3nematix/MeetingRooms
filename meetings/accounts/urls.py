from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from .api import EmployeeViewSet, RegisterAPI

router = routers.DefaultRouter()
router.register('employees', EmployeeViewSet, 'employees')

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += router.urls
