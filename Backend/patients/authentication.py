import requests
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        
        try:
            # Validate token with Auth Service
            response = requests.get(
                f"{settings.AUTH_SERVICE_URL}/api/auth/validate-token",
                headers={'Authorization': auth_header}
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return (user_data, None)
            else:
                raise exceptions.AuthenticationFailed('Token inválido')
                
        except requests.RequestException:
            raise exceptions.AuthenticationFailed('Error de conexión con el servicio de autenticación')