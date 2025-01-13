from django.urls import path
from .views import UserViewSet , RegistrationView , LoginView , TwoStepInRegisterView, UserAvatarUploadView, UserProfileUpdateView, SoftDeleteProfileView, LogoutView, UserRatingsView

urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list_user'}), name='user-list'),
    path('api/users/<int:id>/', UserViewSet.as_view({'get': 'user_by_id'}), name='user-detail'),
    path('api/users/me/', UserViewSet.as_view({'get': 'my_profile'}), name='my-profile'),
    path('api/users/rate/', UserViewSet.as_view({'post': 'rate_user'}), name='rate-user'),
    path('api/users/rate/update/', UserViewSet.as_view({'put': 'rate_user'}), name='update-rating'),
    path('api/users/rate/remove/', UserViewSet.as_view({'delete': 'remove_rating'}), name='remove-rating'),
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/secondregister/', TwoStepInRegisterView.as_view(), name='update-profile'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/users/avatar/', UserAvatarUploadView.as_view(), name='user-avatar-upload'),
    path('api/users/soft-delete/', SoftDeleteProfileView.as_view(), name='soft-delete-profile'),
    path('api/users/profile-update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('api/users/logout/', LogoutView.as_view(), name='logout'),
    path('api/users/top-list/', UserViewSet.as_view({'get': 'top_users'}), name='top-users'),
    path('api/users/all-ratings-user/', UserRatingsView.as_view(), name='user_ratings')
]