from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
User = get_user_model()


class Recipe(models.Model):

    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    photo = CloudinaryField('recipe_photo', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
