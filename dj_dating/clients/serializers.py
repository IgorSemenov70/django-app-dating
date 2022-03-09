from typing import Dict

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from . import services
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализатор регистрации участника и создания нового """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'gender', 'avatar', 'token', 'longitude',
                  'latitude')

    def create(self, validated_data: Dict[str, str]):
        """ Метод для создания нового пользователя """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа участника в систему"""
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data: Dict[str, str]) -> Dict[str, str]:
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
            'token': Token.objects.get(user=user).key
        }


class ClientListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка участников"""
    is_fan = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'gender', 'avatar', 'is_fan', 'distance')

    def get_is_fan(self, obj):
        """Проверяет, лайкнул ли участник другого участника"""
        user = self.context.get('request').user
        return services.is_fan(obj, user)

    def get_distance(self, obj):
        """Показывает расстояние от участника до другого участника"""
        user = self.context.get('request').user
        if user.is_anonymous:
            return
        another_user = get_object_or_404(User, pk=obj.id)
        return services.get_distance_between_clients(
            lon_1=user.longitude,
            lat_1=user.latitude,
            lon_2=another_user.longitude,
            lat_2=another_user.latitude
        )
