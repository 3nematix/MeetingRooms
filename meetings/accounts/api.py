from .models import Employees
from django.http import JsonResponse
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import EmployeeSerializer, RegisterSerializer, LoginSerializer

# Knox
from knox.models import AuthToken


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()

        return Response({
            "employee": EmployeeSerializer(employee, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(employee)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.validated_data

        return Response({
            "employee": EmployeeSerializer(employee,
                                           context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(employee)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_object(self):
        return self.request.user


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]

    queryset = Employees.objects.all()
    serializer_class = EmployeeSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
