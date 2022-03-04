import os

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from imagekit.models.fields import ProcessedImageField
from pilkit.processors import ResizeToFit
from rest_framework.authtoken.models import Token

from .utils import Watermark


def get_path_upload_avatar(instance, file):
    """
    Возвращает путь к загруженному изображению в след.формате:
     (media)/profile_pics/user_1/myphoto_2018-12-2.png
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

    def create_user(self, first_name, last_name, email, gender, avatar=None, password=None):
        """ Создает и возвращает пользователя с имэйлом, паролем, токеном, именем и фамилией. """
        if first_name is None:
            raise TypeError('Users must have an first_name address.')

        if last_name is None:
            raise TypeError('Users must have an last_name address.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=self.normalize_email(email),
                          gender=gender,
                          avatar=avatar)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)

        return user

    def create_superuser(self, first_name, last_name, email, password):
        """ Создает и возвращет пользователя с привилегиями суперадмина. """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(first_name, last_name, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Модель участника """
    email = models.EmailField(db_index=True, unique=True, help_text='Электронная почта')
    first_name = models.CharField(max_length=150, help_text='Имя')
    last_name = models.CharField(max_length=150, help_text='Фамилия')
    gender = models.CharField(max_length=10, help_text='Пол')
    avatar = ProcessedImageField(upload_to=get_path_upload_avatar,
                                 blank=True,
                                 null=True,
                                 help_text='Аватар',
                                 processors=[
                                     ResizeToFit(1000, 1000, upscale=False),
                                     Watermark()
                                 ],
                                 format='JPEG')
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
