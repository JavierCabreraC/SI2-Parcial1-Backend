import jwt
from datetime import datetime, timedelta
from django.conf import settings



def generate_jwt_token(usuario_id, rol):
    payload = {
        "sub": usuario_id,  # ID del usuario
        "rol": rol,  # Rol del usuario
        "exp": datetime.utcnow() + timedelta(minutes=60),  # Expiración del token
        "iat": datetime.utcnow(),  # Fecha de emisión
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

