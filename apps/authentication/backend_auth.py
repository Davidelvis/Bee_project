import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom JWT authentication class.
    """
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication.

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.

        2) `(user, token)` - We return a user/token combination when
                             authentication is successful.

                            If neither case is met, that means there's an error
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed`
                            exception and let Django REST Framework
                            handle the rest.
        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None
        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)
    
    def _authenticate_credentials(self, request, token):
        """
        Authenticate the request using the passed in `token`.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, options={"verify_signature": False})

        except BaseException:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)
        
        try:
            user = User.objects.get(email=payload['email'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)
        
        if not user.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)
        
        return (user, token)