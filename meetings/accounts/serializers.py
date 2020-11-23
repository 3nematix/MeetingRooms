from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Employees, EmployeeManager
import re


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('id', 'public_id', 'first_name',
                  'last_name', 'email_address', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        employee = EmployeeManager.create_user(self.validated_data['first_name'], self.validated_data['last_name'],
                                               self.validated_data['email_address'], self.validated_data['password'])
        return employee

# Registration Serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('id', 'first_name', 'last_name', 'email_address', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        employee = EmployeeManager.create_user(self.validated_data['first_name'], self.validated_data['last_name'],
                                               self.validated_data['email_address'], self.validated_data['password'])
        return employee

# Login Serializer


class LoginSerializer(serializers.Serializer):
    email_address = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        employee = authenticate(**data)
        if employee and employee.is_active:
            return employee
        raise serializers.ValidationError("Incorrect Credentials")
