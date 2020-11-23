from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from accounts.validators import validate_name, validate_password
from django.db import models
import datetime
import uuid


class EmployeeManager(BaseUserManager):
    @staticmethod
    def create_user(first_name, last_name, email_address, password):
        if not first_name or not last_name or not password or not email_address:
            raise ValueError('Not enough values')

        user_obj = Employees(
            first_name=first_name,
            last_name=last_name,
            password=Employees.create_password(password),
            email_address=email_address
        )

        user_obj.save()

        return user_obj

    @staticmethod
    def create_superuser(email_address, password):
        if not password or not email_address:
            raise ValueError('Not enough values')

        user_obj = Employees(
            first_name='Admin',
            last_name='Admin',
            is_superuser=True,
            is_staff=True,
            password=Employees.create_password(password),
            email_address=email_address
        )

        user_obj.save()

        return user_obj


class Employees(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, blank=False, null=False, max_length=36)

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(
        max_length=30, blank=False, null=False, validators=[validate_name])
    last_name = models.CharField(
        max_length=30, blank=False, null=False, validators=[validate_name])

    email_address = models.EmailField(
        max_length=320, unique=True, null=False, blank=False)

    password = models.CharField(
        max_length=128, null=False, blank=False, validators=[validate_password])
    date_registered = models.DateTimeField(auto_now_add=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Employees'

    def __str__(self):
        return str(self.id)

    def create_password(password):
        """Create hashed password from given string."""
        return make_password(password, hasher="argon2")

    def check_password(self, password):
        """Check hashed password."""
        return check_password(password, self.password)
