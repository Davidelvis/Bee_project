
from apps.utils.models import TimeStampedModel
from django.db import models




class Profile(TimeStampedModel):

    user = models.OneToOneField(
        'authentication.User', on_delete=models.CASCADE)
    profile_photo = models.ImageField()
    country = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user
