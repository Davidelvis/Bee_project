import jwt
from django.db import models
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):
    """_summary_

    Args:
        BaseUserManager (_type_): _description_
    """
    def create_user(self, email, password, phone_number, username, tenant_domain_schema, name, **extra_fields):
        """_summary_

        Args:
            email (_type_): _description_
            password (_type_): _description_
            **extra_fields (_type_): _description_

        Returns:
            _type_: _description_
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            name=name, 
            username=username, 
            phone_number=phone_number,
            tenant_domain_schema=tenant_domain_schema,
            email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, name, username, tenant_domain_schema, phone_number, **extra_fields):
        """_summary_

        Args:
            email (_type_): _description_
            password (_type_): _description_
            **extra_fields (_type_): _description_

        Returns:
            _type_: _description_
        """
        user = self.create_user(
            name=name,
            username=username,
            phone_number=phone_number,
            tenant_domain_schema=tenant_domain_schema,
            email=self.normalize_email(email)),
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """_summary_

    Args:
        AbstractBaseUser (_type_): _description_
        PermissionsMixin (_type_): _description_
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    username = models.CharField(max_length=255, blank=False, db_index=True, null=False)
    phone_number = models.CharField(max_length=255, db_index=True, blank=False, null=False)
    tenant_domain_schema = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(max_length=255, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'username', 'phone_number', 'tenant_domain_schema']

    #specifying object manager
    objects = UserManager()

    def __str__(self):
        """
        Returns the string representation of the user
        """
        return f'{self.email}, {self.name}'
    
    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of `user.generate_jwt_token()`
        """
        return self._generate_jwt_token()

    def has_perm(self, perm, obj=None):
        """_summary_

        Args:
            perm (_type_): _description_
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """_summary_

        Args:
            app_label (_type_): _description_

        Returns:
            _type_: _description_
        """
        return True

    def get_full_name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.name

    def get_short_name(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.name

    def get_username(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.username

    def get_phone_number(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.phone_number

    def get_tenant_domain_schema(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.tenant_domain_schema

    def get_email(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.email

    def _generate_jwt_token(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')