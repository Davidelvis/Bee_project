from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = serializers.CharField(source='user.country', read_only=True)
    county = serializers.CharField(source='user.county', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)
    postal_code = serializers.CharField(source='user.postal_code', read_only=True)
    location = serializers.CharField(source='user.location', read_only=True)


    class Meta:
        model = Profile
        fields = ['username', 'profile_photo', 'country', 'county', 'city', 'postal_code', 'location']

    def get_profile_photo(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return 'https://static.productionready.io/images/smiley-cyrus.jpg'