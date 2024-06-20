from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    shop = models.CharField(max_length=255, null=True)
    last_changes = models.DateTimeField(auto_now=True, null=True)  
    last_changes_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name