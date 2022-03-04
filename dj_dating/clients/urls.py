from django.urls import path

from . import views

urlpatterns = [
    path('clients/create/', views.RegistrationAPIView.as_view()),
    path('clients/login/', views.LoginAPIView.as_view()),
    path('clients/<int:pk>/match/', views.LikeUserAPIView.as_view()),
    path('list/', views.ClientListAPIView.as_view({'get': 'list'})),
]
