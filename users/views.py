from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    PublicUserSerializer,
    UserRegisterSerializer,
)


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Свой профиль: просмотр и редактирование."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """Профиль по pk: смотреть может любой авторизованный,
    редактировать — только владелец профиля."""

    def get_queryset(self):
        return User.objects.all()

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if int(self.kwargs['pk']) == self.request.user.id:
            return UserProfileSerializer
        return PublicUserSerializer
