# Generated by Django 5.1.3 on 2025-01-16 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_merge_0004_alter_recipe_id_0005_recipe_is_declined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriterecipe',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]