import os

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from imagekit.models.fields import ProcessedImageField
from pilkit.processors import ResizeToFit
from rest_framework.authtoken.models import Token

from .utils import Watermark


def get_path_upload_avatar(instance, file):
    """
    Возвращает путь к загруженному изображению в след.формате:
     media/profile_pics/user_1/myphoto_2018-12-2.png
    """
    time = timezone.now().strftime("%Y-%m-%d")
    end_extention = file.split('.')[-1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + '_' + time + '.' + end_extention
    return os.path.join('profile_avatar', '{0}/{1}').format(instance.email, file_name)


class UserManager(BaseUserManager):
    """ Кастомный класс менеджер """

    def create_user(self, first_name, last_name, email, gender, avatar=None, longitude=None, latitude=None,
                    password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем, токеном, именем и фамилией. """
        if first_name is None:
            raise TypeError('Users must have an first_name.')

        if last_name is None:
            raise TypeError('Users must have an last_name.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if gender is None:
            raise TypeError('Users must have an gender')

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=self.normalize_email(email),
                          gender=gender,
                          avatar=avatar,
                          longitude=longitude,
                          latitude=latitude)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return user

    def create_superuser(self, first_name, last_name, email, gender, password):
        """ Создает и возвращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(first_name, last_name, email, gender, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class Like(models.Model):
    """Модель лайка"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='likes',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель участника """
    email = models.EmailField(db_index=True, unique=True, help_text='Электронная почта')
    first_name = models.CharField(max_length=150, help_text='Имя')
    last_name = models.CharField(max_length=150, help_text='Фамилия')
    gender = models.CharField(max_length=10, help_text='Пол')
    likes = GenericRelation(Like)
    avatar = ProcessedImageField(upload_to=get_path_upload_avatar,
                                 blank=True,
                                 null=True,
                                 help_text='Аватар',
                                 processors=[ResizeToFit(400, 400, upscale=False), Watermark()],
                                 format='JPEG')
    latitude = models.FloatField(null=True, blank=True, help_text='Широта')
    longitude = models.FloatField(null=True, blank=True, help_text='Долгота')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'User'
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        """ Строковое представление модели """
        return self.email

    def get_full_name(self):
        """Возвращает имя и фамилию участника"""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
