from django.contrib.auth.backends import ModelBackend

from accounts.models import Employees


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, email_address=None, password=None, **kwars):
        try:
            employee = Employees.objects.get(email_address=username or email_address)
        except Employees.DoesNotExist:
            return None
        else:
            if employee.check_password(password) is True:
                return employee
        return None

    def get_user(self, uid):
        try:
            return Employees.objects.get(pk=uid)
        except:
            return None