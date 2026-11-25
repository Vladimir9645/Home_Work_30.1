from django.urls import path

from .views import PaymentListView, UserProfileView


urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
