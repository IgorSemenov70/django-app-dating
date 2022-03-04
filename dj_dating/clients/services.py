from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from .models import Like

User = get_user_model()


def add_like(obj, user):
    """ Лайкает obj и если лайки взаимны отправляет уведомления на почту """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
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


def is_fan(obj, user) -> bool:
    """ Проверяет, лайкнул ли user obj """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()
