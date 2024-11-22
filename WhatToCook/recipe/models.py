from django.db import models
from profiles.models import CustomUser

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='recipes/photos/')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
