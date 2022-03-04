from typing import Dict

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации участника и создания нового """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'gender', 'avatar', 'token')

    def create(self, validated_data: Dict[str, str]):
        """ Метод для создания нового пользователя """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа участника в систему"""
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data: Dict[str, str]):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'token': Token.objects.get(user=user).key
        }