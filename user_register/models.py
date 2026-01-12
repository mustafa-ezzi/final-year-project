# user_register/models.py
from django.core.validators import RegexValidator
from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=120)

    phone_regex = RegexValidator(
        regex=r"^((\+92)|(0092))?-?0?3\d{2}-?\d{7}$",
        message="Phone number must be valid Pakistani format",
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_regex]
    )

    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"
