from django.urls import path

from . import views

urlpatterns = [
    path('clients/create/', views.RegistrationAPIView.as_view(), name='create_client'),
    path('clients/login/', views.LoginAPIView.as_view(), name='client_login'),
    path('clients/<int:pk>/match/', views.LikeUserAPIView.as_view(), name='client_match'),
    path('list/', views.ClientListAPIView.as_view({'get': 'list'}), name='clients_list'),
]
