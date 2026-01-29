from django.db import models


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("Men", "Men"),
        ("Women", "Women"),
        ("Kids", "Kids"),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    badge = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="Men")
    image = models.ImageField(
        upload_to="product_images/"
    )  # This remains the "Main" thumbnail

    def __str__(self):
            return self.name
    

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product_gallery/")

    def __str__(self):
        return f"Image for {self.product.name}"