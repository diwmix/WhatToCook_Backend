from rest_framework import serializers
from .models import CustomUser, Rating
from django.contrib.auth.hashers import make_password
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалізатор для рецепту, який визначає поля, що будуть відображатися в API."""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'instructions', 'category', 'subcategory', 'photo', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Сериалізатор для користувача, що включає рецепти, які користувач має в обраних та створених, а також середній рейтинг та кількість рейтингів."""
    favorite_dishes = RecipeSerializer(many=True, read_only=True)
    created_dishes = RecipeSerializer(many=True, read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description', 'social_links', 'age',
                  'allergic_products', 'restricted_products', 'favorite_dishes', 'created_dishes',
                  'average_rating', 'rating_count', 'avatar', 'is_staff', 'is_superuser']


class RatingSerializer(serializers.ModelSerializer):
    """Сериалізатор для рейтингу, який включає зв'язки з користувачем та рецептом"""

    class Meta:
        model = Rating
        fields = ['rating', 'review', 'user', 'rated_by', 'recipe']
        read_only_fields = ['rated_by']

    def validate(self, data):
        if data['user'] == data['rated_by']:
            raise serializers.ValidationError("Ви не можете оцінити себе")
        return data


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериалізатор для реєстрації користувача, включаючи перевірку на унікальність email."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        """Перевірка, чи не використовується вже введений email в базі даних."""
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        """Створення нового користувача з наданими даними, в тому числі з хешованим паролем."""
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=None,
            password=make_password(validated_data['password']),
            is_active = True
        )
        return user


class TwoStepInRegister(serializers.ModelSerializer):
    """Сериалізатор для другого етапу реєстрації користувача, для заповнення додаткових даних."""
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'social_links', 'allergic_products', 'restricted_products','description']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """ Сериалізатор для оновлення профілю користувача. """
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'social_links', 'allergic_products', 'restricted_products','description']

    def update(self, instance, validated_data):
        """ Оновлення атрибутів користувача на основі наданих даних."""
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

