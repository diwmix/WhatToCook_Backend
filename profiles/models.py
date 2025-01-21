from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.db.models import Avg, Q
from cloudinary.models import CloudinaryField
from decimal import Decimal, ROUND_HALF_UP


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    avatar = CloudinaryField('avatar', blank=True, null=True, default="image/upload/v1737444623/default-user-icon-13_ez6cy7.png" )
    age = models.PositiveIntegerField(blank=True, null=True)
    allergic_products = models.TextField(blank=True, null=True)
    restricted_products = models.TextField(blank=True, null=True)
    average_rating = models.FloatField(default=0)
    favorite_dishes = models.ManyToManyField('recipe.Recipe', related_name='favorite_by', blank=True)
    created_dishes = models.ManyToManyField('recipe.Recipe', related_name='author_by', blank=True)
    is_active = models.BooleanField(default=True)  # Для "м'якого видалення"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        """Повертає email користувача як його унікальний ідентифікатор."""
        return self.email

    def update_average_rating(self):
        from recipe.models import Recipe
        ratings = self.ratings.aggregate(average=Avg('rating'))
        # Обчислення середнього рейтингу
        self.average_rating = round(ratings['average'] or 0.0, 2)
        self.save()

    @property
    def rating_count(self):
        """Повертає кількість рейтингів користувача"""
        return self.ratings.count()


class Rating(models.Model):
    """Зберігається оцінка та зв'язок між оцінюваним та оціночним користувачем."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ratings')
    rated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.DecimalField(max_digits=3,  decimal_places=1,  validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('5.0'))]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'rated_by'], name='unique_user_rated_by')
        ]

    def __str__(self):
        return f"Rating {self.rating} from {self.rated_by.email} to {self.user.email}"