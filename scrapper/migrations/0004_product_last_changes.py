# Generated by Django 5.0.6 on 2024-06-19 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0003_product_shop'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_changes',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]