from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    class Meta:
        unique_together = ('name', 'website')

    def __str__(self):
        return f"{self.name} from {self.website}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    shop = models.CharField(max_length=255, null=True)
    last_changes = models.DateTimeField(auto_now=True, null=True)
    last_changes_details = models.TextField(null=True, blank=True)
    category_fk = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # Zmieniono tutaj

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_categories = models.ManyToManyField(Category, blank=True)

    def get_preferred_categories_list(self):
        return self.preferred_categories.all()