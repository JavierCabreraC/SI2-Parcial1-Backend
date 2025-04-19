from django.urls import resolve
from .utils import registrar_accion
from rest_framework_simplejwt.authentication import JWTAuthentication



class BitacoraMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Mapeamos URLs a tipos de acción
        self.url_to_action = {
            'token_obtain_pair': 'Login',
            'usuario-list': 'GenerarReporte',  # Ejemplo para listar usuarios
            'personal-create': 'CrearPersonal',  # Ajustar según corresponda
            'cliente-create': 'CrearCliente',
            # Añadir más mapeos según las URLs y acciones disponibles
            'usuario-out': 'Logout',
            'cliente-read': 'LeerCliente',
            'cliente-update': 'ActualizarCliente',
            'personal-read': 'LeerPersonal',
            'personal-update': 'ActualizarPersonal',
            'usuario-read': 'LeerUsuario',
            'categoria-create': 'CrearCategoria',
            'categoria-read': 'ConsultarCategoria',
            'categoria-update': 'ActualizarCategoria',
            'producto-create': 'CrearProducto',
            'producto-read': 'LeerProducto',
            'producto-update': 'ActualizarProducto',
            'producto-delete': 'EliminarProducto',
            'venta-create': 'CrearVenta',
            'venta-read': 'ConsultarVenta',
            'venta-update': 'CancelarVenta',
            'stock-update': 'ActualizarStock',
            'historial-read': 'ConsultarHistorial',
            'notificacion-create': 'CrearNotificacion',
            'notificacion-read': 'ConsultarNotificacion',
            'notificacion-update': 'ActualizarNotificacion',
            'comando-create': 'CrearComandos',
            'comando-read': 'ConsultarComandos',
        }
        self.jwt_auth = JWTAuthentication()
    
    def __call__(self, request):
        # Obtener la respuesta primero, por si hay errores
        response = self.get_response(request)
        
        try:
            # Solo procesar si la petición fue exitosa
            if 200 <= response.status_code < 300:
                # Intentar obtener el usuario desde el token
                usuario_id = self.get_user_id_from_request(request)
                
                if usuario_id:
                    # Obtener el nombre de la URL actual
                    url_name = self.get_url_name(request)
                    
                    # Si la URL corresponde a una acción que queremos registrar
                    if url_name in self.url_to_action:
                        # Obtener la IP del cliente
                        ip = self.get_client_ip(request)
                        
                        # Registrar la acción
                        registrar_accion(
                            usuario_id=usuario_id,
                            tipo_accion=self.url_to_action[url_name],
                            ip_direccion=ip
                        )
        except Exception as e:
            # No interrumpir la respuesta aunque falle el registro
            print(f"Error en BitacoraMiddleware: {str(e)}")
        
        return response
    
    def get_client_ip(self, request):
        """Obtiene la dirección IP real del cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        return ip
    
    def get_url_name(self, request):
        """Obtiene el nombre de la URL actual."""
        resolver_match = resolve(request.path_info)
        return resolver_match.url_name
    
    def get_user_id_from_request(self, request):
        """Extrae el ID de usuario desde el token JWT."""
        # Primero intentamos desde la autenticación JWT
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                validated_token = self.jwt_auth.get_validated_token(token)
                return validated_token.get('sub')
            except Exception:
                pass
        
        # Si no hay token o es inválido, intentamos desde el usuario autenticado
        if hasattr(request, 'user') and request.user.is_authenticated:
            return request.user.id
        
        return None

