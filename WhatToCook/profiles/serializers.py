from rest_framework import serializers
from .models import CustomUser, Rating
from django.contrib.auth.hashers import make_password
from recipe.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'instructions', 'category', 'subcategory', 'photo', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    favorite_dishes = RecipeSerializer(many=True, read_only=True)
    created_dishes = RecipeSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description', 'social_links', 'age',
                  'allergic_products', 'restricted_products', 'favorite_dishes', 'created_dishes',
                  'average_rating', 'avatar']  # Include avatar field here


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'rated_by', 'rating']
        read_only_fields = ['rated_by']

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            username=None,
            password=make_password(validated_data['password'])
        )
        return user



class TwoStepInRegister(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'age', 'social_links', 'allergic_products', 'restricted_products']