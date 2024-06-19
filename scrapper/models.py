from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    shop = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.name