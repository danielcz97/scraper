# Generated by Django 5.0.6 on 2024-06-20 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrapper', '0004_product_last_changes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_changes_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
