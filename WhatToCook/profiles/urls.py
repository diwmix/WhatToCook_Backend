from django.urls import path
from .views import UserViewSet

urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list_user'}), name='user-list'),
    path('api/users/<int:id>/', UserViewSet.as_view({'get': 'user_by_id'}), name='user-detail'),
    path('api/users/<int:id>/rate/', UserViewSet.as_view({'post': 'rate_user'}), name='rate-user'),
]