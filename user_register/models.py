from django.db import models
from django.core.validators import RegexValidator

# user_register/models.py
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
