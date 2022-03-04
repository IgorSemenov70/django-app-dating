from django_filters import rest_framework as filters

from .models import User


class ClientsFilter(filters.FilterSet):
    """ Фильтр для вывода списка участников по полу, имени и фамилии """
    gender = filters.CharFilter(field_name='gender', lookup_expr='iexact')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='iexact')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='iexact')

    class Meta:
        model = User
        fields = ('gender', 'first_name', 'last_name')
