from django.core.exceptions import ValidationError
import re


def validate_name(value):
    if not re.match(r"^[A-Z]{1}[a-z]{2,25}$", value):
        raise ValidationError("Please check your Last Name")
    return value


def validate_password(value):
    if " " in value:
        raise ValidationError("Password cannot contain any spaces")
    return value
