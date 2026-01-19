from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class Customer(models.Model):
    DELIVERY_CHOICES = [
        ('home', 'Home Delivery'),
        ('pickup', 'Store Pickup'),
    ]

    # Basic identity
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='NA')

    # Contact
    email = models.EmailField(unique=True)

    phone_regex = RegexValidator(
        regex=r'^03\d{9}$',
        message='Enter valid Pakistani number (03XXXXXXXXX)'
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_regex]
    )

    # Delivery info
    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES
    )
    address = models.TextField(blank=True)

    # Meta info (VERY IMPORTANT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.delivery_type == 'home' and not self.address:
            raise ValidationError("Address is required for home delivery")

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"
    


    delivery_type = models.CharField(
        max_length=10,
        choices=DELIVERY_CHOICES,
        default='home'  # <--- add this
)

