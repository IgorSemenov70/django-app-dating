from typing import Union, List

from django.db.models.query import QuerySet
from django.views import View
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request

from .models import User
from .services import get_distance_between_clients


class ClientsFilter(filters.FilterSet):
    """ Фильтр для вывода списка участников по полу, имени и фамилии """
    gender = filters.CharFilter(field_name='gender', lookup_expr='iexact')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='iexact')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='iexact')
    distance = filters.NumberFilter(field_name='distance', lookup_expr='lte')

    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name', 'distance')


class DistanceBetweenClientsFilter(DjangoFilterBackend):
    """Фильтр для вывода списка участников находящихся на заданной дистанции друг от друга"""

    def filter_queryset(self, request: Request, queryset: QuerySet, view: View) -> Union[QuerySet, List]:
        another_users = queryset
        new_queryset = []
        distance_param = request.GET.get('distance')
        if distance_param and bool(float(distance_param)):
            for user in another_users:
                current_user_long = request.user.longitude
                current_user_lat = request.user.latitude
                another_user_long = user.longitude
                another_user_lat = user.latitude
                distance = get_distance_between_clients(current_user_long, current_user_lat, another_user_long,
                                                        another_user_lat)
                if distance < float(distance_param):
                    new_queryset.append(user)
            return new_queryset
        return queryset
