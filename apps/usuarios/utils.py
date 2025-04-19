import jwt
from django.conf import settings
from datetime import datetime, timedelta
from .models import Bitacora, TipoAccionBitacora, Usuario



def generate_jwt_token(usuario_id, rol):
    payload = {
        "sub": usuario_id,  # ID del usuario
        "rol": rol,  # Rol del usuario
        "exp": datetime.utcnow() + timedelta(minutes=60),  # Expiración del token
        "iat": datetime.utcnow(),  # Fecha de emisión
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token



def registrar_accion(usuario_id, tipo_accion, ip_direccion):
    """
    Registra una acción en la bitácora
    
    Args:
        usuario_id: ID del usuario que realiza la acción
        tipo_accion: String con el tipo de acción (debe coincidir con AccionChoices)
        ip_direccion: Dirección IP desde donde se realiza la acción
    """
    try:
        # Obtener o crear el tipo de acción
        tipo_accion_obj, _ = TipoAccionBitacora.objects.get_or_create(
            accion=tipo_accion
        )
        
        # Crear el registro en la bitácora
        Bitacora.objects.create(
            usuario_id=usuario_id,
            tipo_accion=tipo_accion_obj,
            ip_direccion=ip_direccion
        )
        
        return True
    except Exception as e:
        print(f"Error al registrar acción en bitácora: {str(e)}")
        return False