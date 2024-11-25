from rest_framework import serializers
from .models import Recipe
from profiles.serializers import UserSerializer

class RecipeRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=50),
        allow_empty=False
    )

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        author = UserSerializer(read_only=True)
        model = Recipe
        fields = [
            'id','title','ingredients','instructions','category','subcategory','photo','author','is_approved','created_at',
        ]
        