# Generated by Django 5.1.3 on 2024-11-23 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='created_dishes',
            field=models.ManyToManyField(blank=True, null=True, related_name='author_by', to='recipe.recipe'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='favorite_dishes',
            field=models.ManyToManyField(blank=True, related_name='favorite_by', to='recipe.recipe'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]