# user_register/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomerManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    username = None  # remove username

    email = models.EmailField(unique=True)
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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomerManager()

    def __str__(self):
        return self.email

