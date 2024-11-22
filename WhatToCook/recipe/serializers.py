from rest_framework import serializers

class RecipeRequestSerializer(serializers.Serializer):
    ingredients = serializers.ListField(
        child=serializers.CharField(max_length=50),
        allow_empty=False
    )
