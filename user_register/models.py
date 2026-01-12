# user_register/models.py
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class Customer(AbstractUser):
    # Remove username if you don't want to use it
    username = None
    USERNAME_FIELD = "email"  # login with email
    REQUIRED_FIELDS = ["name"]  # fields required when creating superuser

    name = models.CharField(max_length=120)

    phone_regex = RegexValidator(
        regex=r"^((\+92)|(0092))?-?0?3\d{2}-?\d{7}$",
        message="Phone number must be valid Pakistani format",
    )
    phone_number = models.CharField(
        max_length=15, unique=True, blank=True, null=True, validators=[phone_regex]
    )

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    # Timestamps (optional but useful)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email or self.name
