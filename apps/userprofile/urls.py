from django.urls import path

from .views import ProfileRetrieveAPIView

app_name = 'userprofile'

urlpatterns = [
    path('profiles/<int:user_id>', ProfileRetrieveAPIView.as_view()),
]