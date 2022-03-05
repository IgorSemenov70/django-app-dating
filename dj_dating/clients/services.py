from math import sin, cos, radians, acos
from typing import Dict

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import Like

User = get_user_model()


def add_like(obj: User, user: User) -> Dict[str, str]:
    """ Лайкает другого участника и если лайки взаимны отправляет уведомления на почту """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, user=user)
    if is_fan(obj, user):
        liked_user = get_object_or_404(User, pk=obj.id)
        send_mail(
            subject='Уведомление о симпатии',
            message=f'Вы понравились {user.get_full_name()}! Почта участника {user.email}',
            from_email=user.email,
            recipient_list=[liked_user.email]
        )
        send_mail(
            subject='Уведомление о симпатии',
            message=f'Вы понравились {liked_user.get_full_name()}! Почта участника {liked_user.email}',
            from_email=liked_user.email,
            recipient_list=[user.email]
        )
        return {'email': obj.email}
    return {'message': 'like added'}


def is_fan(obj: User, user: User) -> bool:
    """ Проверяет, лайкнул ли участник другого участника """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_distance_between_clients(lon_1: float, lat_1: float, lon_2: float, lat_2: float) -> float:
    """Определяет расстояние между участниками"""
    lon_1, lat_1, lon_2, lat_2 = map(radians, [lon_1, lat_1, lon_2, lat_2])
    distance = 6371 * (acos(sin(lat_1) * sin(lat_2) + cos(lat_1) * cos(lat_2) * cos(lon_1 - lon_2)))
    return round(distance, 4)
