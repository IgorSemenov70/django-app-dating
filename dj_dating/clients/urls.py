from django.urls import path

from . import views


urlpatterns = [
    path('clients/create/', views.RegistrationAPIView.as_view()),
    path('clients/login/', views.LoginAPIView.as_view()),
]