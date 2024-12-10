from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
from cloudinary.models import CloudinaryField


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    allergic_products = models.TextField(blank=True, null=True)
    restricted_products = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(default=0)
    favorite_dishes = models.ManyToManyField('recipe.Recipe', related_name='favorite_by', blank=True)
    created_dishes = models.ManyToManyField('recipe.Recipe', related_name='author_by', blank=True, default=0)

    def __str__(self):
        return self.email

    def update_average_rating(self):
        from recipe.models import Recipe
        ratings = self.ratings.aggregate(Avg('rating'))
        self.average_rating = ratings['rating__avg'] if ratings['rating__avg'] is not None else 0.0
        self.save()


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'rated_by')  # Щоб один користувач не міг оцінити > одного разу
