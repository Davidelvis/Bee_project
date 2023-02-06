from django.urls import path
from . import views

app_name = 'authentication'
urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UserRetrieveUpdateAPIView.as_view()),
]