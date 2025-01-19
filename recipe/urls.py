from django.urls import path
from .views import GenerateRecipeView, RecipeCreateView, PublishedRecipesView, RecipeSearchView, RecipeDeleteView, RecipeDetailView, RecipeListView, ReviewView, FavoriteRecipeView, RecipeApproveView, RecipeDisapproveView, RecipeEditView, NotPublishedRecipesView
urlpatterns = [
    path('api/recipes/generate/', GenerateRecipeView.as_view(), name='recipe'),
    path('api/recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('api/recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('api/recipes/<pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('api/recipes/<pk>/update/', RecipeEditView.as_view(), name='recipe-update'),
    path('api/recipes/published/', PublishedRecipesView.as_view(), name='recipe-list'),
    path('api/recipes/not-published/', NotPublishedRecipesView.as_view(), name='recipe-list'),
    path('api/recipes/search/', RecipeSearchView.as_view(), name='recipe-search'),
    path('api/recipes/<pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('api/recipes/<pk>/reviews/', ReviewView.as_view(), name='recipe-review'),
    path('api/recipes/<pk>/favorite/', FavoriteRecipeView.as_view(), name='favorite-recipe'),
    path('api/recipes/<pk>/favorite/', FavoriteRecipeView.as_view(), name='favorite-recipe-delete'),
    path('api/recipes/approved/<pk>/', RecipeApproveView.as_view(), name='recipe-approve'),
    path('api/recipes/disapproved/<pk>/', RecipeDisapproveView.as_view(), name='recipe-disapprove'),
]
 