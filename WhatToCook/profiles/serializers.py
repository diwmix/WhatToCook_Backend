from rest_framework import serializers
from .models import CustomUser, Rating, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    favorite_dishes = ProductSerializer(many=True, read_only=True)
    created_dishes = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description', 'social_links', 'age',
                  'allergic_products', 'restricted_products', 'favorite_dishes', 'created_dishes',
                  'average_rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'rated_by', 'rating']
        read_only_fields = ['rated_by']
