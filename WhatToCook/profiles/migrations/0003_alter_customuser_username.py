# Generated by Django 5.1.3 on 2024-11-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_delete_product_remove_customuser_is_admin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, unique=True),
        ),
    ]