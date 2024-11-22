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
            prompt = f"Зроби {', '.join(ingredients)}"
            
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
