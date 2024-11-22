from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)

    is_admin = models.BooleanField(default=False)
    name = models.TextField(blank=False)
    email = models.EmailField(unique=True)

    description = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    allergic_products = models.TextField(blank=True, null=True)
    restricted_products = models.TextField(blank=True, null=True)

    average_rating = models.FloatField(default=0)

    def update_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            self.average_rating = sum(r.rating for r in ratings) / ratings.count()
        else:
            self.average_rating = 0
        self.save()


class Product(models.Model):
    name = models.CharField(max_length=255)


class Rating(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('user', 'rated_by')  # Щоб один користувач не міг оцінити > одного разу
