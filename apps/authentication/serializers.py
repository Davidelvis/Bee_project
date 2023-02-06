from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from apps.userprofile.serializers import ProfileSerializer



class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a user.
    """
    # The password field is write only and will not be returned in the response and cannot be read by the client

    username = serializers.CharField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    
    # The token field is for storing the token that we will send back to the user
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # The fields that we want to include in our serializer
        fields = ['username', 'password', 'token', 'email', 'name', 'phone_number', 'tenant_domain_schema']

    def create(self, validated_data):
        # Create a new user using the `create_user` helper method. This method is provided by Django
        return User.objects.create_user(**validated_data)
    
"""
The Login Serializer
"""

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, required=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    tenant_domain_schema = serializers.CharField(max_length=255, read_only=True)

    def validate(self, attrs):
        """_summary_

        Args:
            attrs (_type_): _description_

        Raises:
            serializers.ValidationError: _description_
            serializers.ValidationError: _description_

        Returns:
            _type_: _description_
        """
        email = attrs.get('email', None)
        tenant_domain_schema = attrs.get('tenant_domain_schema', None)
        password = attrs.get('password', None)

        # If email is not provided, raise an error
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        # If password is not provided, raise an error
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        
        user = authenticate(email=email, password=password)
       
        # If a user with this email and password is not found, raise an error
        if not user:
            raise serializers.ValidationError(
                'Invalid email or password, please try again'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'Account disabled, contact admin'
            )
        return {
            'email': user.email,
            'token': user.token,
            'tenant_domain_schema': user.tenant_domain_schema
        }


class UserSerializer(serializers.ModelSerializer):
    """
    serializer for user model
    """
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    profile = ProfileSerializer(write_only=True)
    profile_photo = serializers.CharField(source='profile.profile_photo', read_only=True)
    country = serializers.CharField(source='profile.country', read_only=True)
    county = serializers.CharField(source='profile.county', read_only=True)
    city = serializers.CharField(source='profile.city', read_only=True)
    postal_code = serializers.CharField(source='profile.postal_code', read_only=True)
    location = serializers.CharField(source='profile.location', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'username', 'phone_number', 'tenant_domain_schema' 'email', 'password',
                  'token', 'profile', 'profile_photo', 'country', 'county', 'city', 'postal_code', 'location']

        read_only_fields = ('token', )

    def update(self, instance, validated_data):
        """
        Update a user, setting the password correctly and return it
        """

        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        if password is not None:
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)
        
        #save profile
        instance.profile.save()

        return super().update(instance, validated_data)