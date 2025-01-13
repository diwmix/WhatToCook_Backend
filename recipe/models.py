from django.db import models
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
import uuid

User = get_user_model()


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=None, editable=False)
    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    photo = CloudinaryField('recipe_photo', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Якщо ID ще не згенеровано
            self.id = self.generate_random_id()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_random_id():
        return uuid.uuid4()

    def __str__(self):
        return self.title


class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.recipe.title}"