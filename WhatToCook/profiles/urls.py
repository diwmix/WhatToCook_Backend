from django.urls import path
from .views import UserViewSet , RegistrationView , LoginView , TwoStepInRegisterView

urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list_user'}), name='user-list'),
    path('api/users/<int:id>/', UserViewSet.as_view({'get': 'user_by_id'}), name='user-detail'),
    path('api/users/<int:id>/rate/', UserViewSet.as_view({'post': 'rate_user'}), name='rate-user'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/secondregister/', TwoStepInRegisterView.as_view(), name='update-profile'),
]