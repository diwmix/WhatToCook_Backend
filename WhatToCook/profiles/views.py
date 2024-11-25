from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser, Rating
from .serializers import UserSerializer, RatingSerializer, RegistrationSerializer, TwoStepInRegister
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

    def user_by_id(self, request, id=None):
        try:
            user = CustomUser.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def rate_user(self, request, id=None):
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            return Response({"error": "Користувача не знайдено"}, status=404)

        if user == request.user:
            return Response({"error": "Ви не можете оцінити себе"}, status=400)

        existing_rating = Rating.objects.filter(user=user, rated_by=request.user).first()

        if existing_rating:
            if request.data.get("action") == "remove":
                existing_rating.delete()
                user.update_average_rating()
                return Response({'status': 'Оцінку видалено', 'average_rating': user.average_rating})
            serializer = RatingSerializer(existing_rating, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                user.update_average_rating()
                return Response({'status': 'Оцінку оновлено', 'average_rating': user.average_rating})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rated_by=request.user, user=user)
        user.update_average_rating()

        return Response({'status': 'Оцінку додано', 'average_rating': user.average_rating})

    ##  {
    #   "action": "remove"
    #   }
    # якшо в запиті буде так , то це забере оцінку
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
    permission_classes = []
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class TwoStepInRegisterView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = TwoStepInRegister(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)