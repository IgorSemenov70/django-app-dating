from django.db.models.query import QuerySet
from rest_framework import permissions, generics
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from . import services
from .filters import ClientsFilter, DistanceBetweenClientsFilter
from .models import User
from .serializers import RegistrationSerializer, LoginSerializer, ClientListSerializer


class RegistrationAPIView(generics.GenericAPIView):
    """Представление для регистрации участника"""
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    """Представление для входа в систему участника"""
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeUserAPIView(generics.GenericAPIView):
    """Представление для проставления лайка участнику"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClientListSerializer
    queryset = ''

    def post(self, request: Request, pk: int = None) -> Response:
        obj = User.objects.get(id=pk)
        return Response(services.add_like(obj, request.user), status=status.HTTP_200_OK)


class ClientListAPIView(viewsets.ReadOnlyModelViewSet):
    """Представление для вывода участников"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ClientListSerializer
    filter_backends = (DistanceBetweenClientsFilter,)
    filterset_class = ClientsFilter

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_authenticated:
            queryset = User.objects.filter(is_active=True).exclude(email=self.request.user.email)
        else:
            queryset = User.objects.filter(is_active=True)
        return queryset
