from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PaymentListView,
    UserProfileView,
    UserProfileDetailView,
    UserRegisterView,
)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', UserProfileDetailView.as_view(), name='profile-detail'),
]
