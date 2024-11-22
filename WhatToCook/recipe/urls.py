from django.urls import path
from .views import RecipeView

urlpatterns = [
    path('api/recipe/', RecipeView.as_view(), name='recipe'),
]
