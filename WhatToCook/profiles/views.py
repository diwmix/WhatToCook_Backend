from rest_framework import viewsets , status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser, Rating
from .serializers import UserSerializer, RatingSerializer, RegistrationSerializer, TwoStepInRegister
from rest_framework.permissions import IsAuthenticated


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
            return Response({"error": "User not found"}, status=404)

        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(rated_by=request.user, user=user)
        user.update_average_rating()
        return Response({'status': 'Rating added', 'average_rating': user.average_rating})


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Registration successful. Check your email for verification."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):  # змінили на 'post'
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=email, password=password)  # Замінили CustomUser на user
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class TwoStepInRegisterView(APIView):
    def post(self, request):
        serializer = TwoStepInRegister(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)