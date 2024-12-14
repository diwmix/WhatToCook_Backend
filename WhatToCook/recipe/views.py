from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq
from .serializers import RecipeRequestSerializer , RecipeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.generics import ListAPIView
from .models import Recipe, Review
from .serializers import RecipeSerializer, ReviewSerializer


client = Groq(
    api_key="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"
)

class GenerateRecipeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RecipeRequestSerializer(data=request.data)
        if serializer.is_valid():
            ingredients = serializer.validated_data['ingredients']
            
            user = request.user
            allergy_ingredients = user.allergic_products

            allergy_warning = (f"У мене алергія на наступні інгредієнти: {', '.join(allergy_ingredients)}. "
                               if allergy_ingredients else "")

            prompt = (f"Ти кухар найкращого ресторану у світі та працюєш на сайт What To Cook. {allergy_warning}"
                      f"Дай мені пораду, яку страву я можу приготувати з цих інгредієнтів: {', '.join(ingredients)}."
                      f"На мої інші питання ти відповідаєш, що ти тільки кухар, який допомагає придумати рецепт. "
                      f"Якщо замість рецепту я вводжу неїстівні продукти, то ти кажеш, що з цього не можна нічого зробити та відразу пишеш будь-який інший рецепт на свій погляд."
                      f"Формат, у якому ти маєш мені повертати рецепт, має складатись з:"
                      f"1) Короткий опис страви. 2) Інгредієнти. 3) Рецепт приготування."
                      f"Та завжди в кінці пиши * З любов'ю Саша")

            try:
                # Send request to Groq API
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-70b-versatile",
                )

                # Process response
                if hasattr(response, 'choices') and response.choices:
                    recipe = response.choices[0].message.content
                else:
                    return Response({"error": "Некоректна відповідь від Groq API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({"recipe": recipe}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecipeCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = RecipeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PublishedRecipesView(ListAPIView):
    queryset = Recipe.objects.filter(is_approved=True).order_by('-created_at')
    serializer_class = RecipeSerializer


class RecipeSearchView(APIView):
    def get(self, request):
        query = request.GET.get('query')
        if query:
            recipes = Recipe.objects.filter(title__icontains=query) | Recipe.objects.filter(ingredients__icontains=query)
            serializer = RecipeSerializer(recipes, many=True)
            return Response(serializer.data)
        return Response(query)


class RecipeDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            if recipe.author == request.user | request.user.is_superuser:
                recipe.delete()
                return Response({"message": "Recipe deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You are not the author of this recipe"}, status=status.HTTP_403_FORBIDDEN)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        

class RecipeDetailView(APIView):
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Recipe.DoesNotExist:
            return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
        

class RecipeListView(APIView):
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        user = request.user
        review_text = request.data.get('review_text')
        rating = request.data.get('rating')

        review = Review.objects.create(
            recipe=recipe,
            user=user,
            review_text=review_text,
            rating=rating
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)