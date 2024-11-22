from rest_framework import viewsets
from rest_framework.response import Response
from .models import CustomUser, Rating
from .serializers import UserSerializer, RatingSerializer

class UserViewSet(viewsets.ViewSet):

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
