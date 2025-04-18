from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import Usuario



class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['sub']
            user = Usuario.objects.get(id=user_id)
            
            if user.estado != 'activo':
                raise AuthenticationFailed('Usuario inactivo o eliminado')
                
            return user
        except Usuario.DoesNotExist:
            raise AuthenticationFailed('Usuario no encontrado')
