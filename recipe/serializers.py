from random import random

from rest_framework import serializers
from .models import Recipe, Review, FavoriteRecipe
from profiles.serializers import UserSerializer

class RecipeRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=50),
        allow_empty=False
    )


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'recipe', 'user', 'review_text', 'rating', 'created_at']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    class Meta:
        model = Recipe
        fields = [
            'id','title','ingredients','instructions','category','subcategory','photo','author','is_approved','created_at','reviews',
        ]

        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'recipe', 'user', 'review_text', 'rating', 'created_at']

class FavoriteRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()  # Вложенный сериализатор для получения деталей рецепта

    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'user', 'recipe', 'created_at']

