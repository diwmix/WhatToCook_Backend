# Generated by Django 5.1.3 on 2025-01-13 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_alter_recipe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='id',
            field=models.UUIDField(default=None, editable=False, primary_key=True, serialize=False),
        ),
    ]
