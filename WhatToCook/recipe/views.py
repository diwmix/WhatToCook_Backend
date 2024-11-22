from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from groq import Groq
from .serializers import RecipeRequestSerializer

client = Groq(
    api_key="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"
)

class RecipeView(APIView):
    def post(self, request):
        serializer = RecipeRequestSerializer(data=request.data)
        if serializer.is_valid():
            ingredients = serializer.validated_data['ingredients']
            prompt = f"Ти кухар найкращого ресторану у світі та працюєш на сайт What To Cook. Дай мені пораду , яку страву я можу приготувати з цих інградієнітів {', '.join(ingredients)}. На мої інші питання , ти відповідаєш , шо ти тільки кухар, який допомагає придумати рецепт . Якщо замість рецепту я вводжу неїстівні продукти , то ти кажеш, шо з цього не можна нічого зробити та відразу пишеш любий інший рецепт на свій погляд.Формат в якому ти маєш мені повертати рецепт має складатись  1)Короткий опис страви. 2)Інградієнти. 3)Рецепт приготування.Та завжди в кінці Пиши * З любов'ю Сайт What To Cook"
            
            try:
                # Отправляем запрос к Groq API
                response = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    model="llama-3.1-70b-versatile",
                )

                # Корректное извлечение данных
                if hasattr(response, 'choices') and response.choices:
                    recipe = response.choices[0].message.content
                else:
                    return Response({"error": "Некорректный ответ от Groq API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({"recipe": recipe}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
