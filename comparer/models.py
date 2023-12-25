from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller_type = models.CharField(max_length=255)
    product_url = models.URLField()
    image_url = models.URLField()

    def __str__(self):
        return self.title

