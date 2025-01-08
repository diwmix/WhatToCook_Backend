from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser, Rating
from .serializers import UserSerializer, RatingSerializer, RegistrationSerializer, TwoStepInRegister, UserProfileUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list_user(self, request):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def my_profile(self, request):
        """
        Інформація для отримання інформації про користувача
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def user_by_id(self, request, id=None):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def rate_user(self, request):
        """Оцінювання користувача"""

        # Отримання даних з запиту
        user_id = request.data.get("user")
        rated_by_id = request.data.get("rated_by")
        rating_value = request.data.get("rating")

        if not user_id or not rated_by_id or rating_value is None:
            return Response({"error": "Не всі необхідні дані надано"}, status=400)

        try:
            # Знайдемо користувача, якому ставлять оцінку
            user = CustomUser.objects.get(id=user_id)

            # Знайдемо користувача, який ставить оцінку
            rated_by = CustomUser.objects.get(id=rated_by_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=404)

        # Перевірка, чи не оцінює користувач сам себе
        if user == rated_by:
            return Response({"error": "Ви не можете оцінити себе"}, status=400)

        # Додавання або оновлення рейтингу
        return self.add_or_update_rating(request, user, rated_by, rating_value)

    def add_or_update_rating(self, request, user, rated_by, rating_value):
        """Додавання або оновлення рейтингу"""
        existing_rating = Rating.objects.filter(user=user, rated_by=rated_by).first()

        # Якщо рейтинг вже існує, оновимо його
        if existing_rating:
            serializer = RatingSerializer(existing_rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                user.update_average_rating()
                return Response({'status': 'Оцінку оновлено', 'average_rating': user.average_rating})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Створення нового рейтингу
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rated_by=rated_by, user=user, rating=rating_value)
        user.update_average_rating()
        return Response({'status': 'Оцінку додано', 'average_rating': user.average_rating})

class UserAvatarUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        avatar = request.FILES.get('avatar')  # Get avatar file from the request
        if avatar:
            user.avatar = avatar  # Save avatar to Cloudinary
            user.save()
            return Response({"message": "Avatar updated successfully.", "avatar_url": user.avatar.url})
        return Response({"error": "No avatar file provided."}, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {"message": "Registration successful.", "token": token.key},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email і пароль є обов'язковими."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Аутентифікація
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # Генерація або отримання токена
            token, created = Token.objects.get_or_create(user=user)

            # Додавання додаткових даних до відповіді
            user_data = UserSerializer(user).data
            return Response({
                "message": "Успішний вхід.",
                "token": token.key,
                "user": user_data
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Невірні дані для входу."},
            status=status.HTTP_401_UNAUTHORIZED
        )


class TwoStepInRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TwoStepInRegister(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SoftDeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # Якщо користувач уже видалений, не даємо можливості видаляти профіль повторно
        if not user.is_active:
            return Response({"error": "Your account is already deactivated."}, status=status.HTTP_400_BAD_REQUEST)

        # М'яке видалення профілю
        user.is_active = False
        user.save()

        return Response({"message": "Your account has been deactivated successfully."}, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Отримати дані профілю поточного користувача.
        """
        serializer = UserProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        """
        Оновити дані профілю поточного користувача.
        """
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)