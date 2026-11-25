from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = serializers.StringRelatedField()
    paid_lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ['payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class UserProfileSerializer(serializers.ModelSerializer):
    """Свой профиль: всё, включая email, фамилию и платежи."""
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'city', 'payments']


class PublicUserSerializer(serializers.ModelSerializer):
    """Чужой профиль: email и фамилию не показываем, но историю платежей показываем."""
    payments = PaymentSerializer(source='payment_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'city', 'payments']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
