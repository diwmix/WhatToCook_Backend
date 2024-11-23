from django.urls import path
from .views import RecipeView, RecipeCreateView, PublishedRecipesView

urlpatterns = [
    path('api/recipe/', RecipeView.as_view(), name='recipe'),
    path('api/recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('api/recipes/', PublishedRecipesView.as_view(), name='recipe-list'),
]
