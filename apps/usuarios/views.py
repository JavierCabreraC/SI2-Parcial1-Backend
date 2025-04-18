from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario, Cliente, Personal
from .serializers import UsuarioSerializer, UsuarioCreateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdminUser
from .serializers import ClienteCreateSerializer, PersonalCreateSerializer



## LOGIN VIEW
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email y contraseña son requeridos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Buscar el usuario por email
        usuario = encontrar_usuario(email)

        # Verificar la contraseña
        if not check_password(password, usuario.password):
            return Response({"error": "Contraseña incorrecta"}, status=status.HTTP_401_UNAUTHORIZED)

        # Usar SimpleJWT para generar tokens
        refresh = RefreshToken.for_user(usuario)
        
        # Agregar claims personalizados
        refresh['rol'] = usuario.rol

        return Response({
            "refresh": str(refresh),
            "access_token": str(refresh.access_token),
            "rol": usuario.rol
        }, status=status.HTTP_200_OK)

    except Usuario.DoesNotExist:
        return Response({"error": "El correo ingresado no tiene un usuario asociado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


## Helper function to find user by email
def encontrar_usuario(email):
    # Buscar en la tabla Cliente
    cliente = Cliente.objects.filter(email=email).first()
    if cliente:
        return Usuario.objects.get(cliente=cliente, estado='activo')

    # Buscar en la tabla Personal
    personal = Personal.objects.filter(email=email).first()
    if personal:
        return Usuario.objects.get(personal=personal, estado='activo')

    raise Usuario.DoesNotExist("Usuario no encontrado")


## *********************************************************************************************
## CREAR VIEWS:

## CREAR PERSONAL
class PersonalCreateView(APIView):
    permission_classes = [ IsAdminUser ]
    
    def post(self, request):
        serializer = PersonalCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Crear el personal
            personal = serializer.save()
            
            # Crear usuario asociado al personal
            usuario_data = {
                'password': make_password('temporal123'),  # Contraseña temporal
                'rol': 'almacenista',  # Rol por defecto para personal
                'estado': 'activo',
                'personal': personal
            }
            
            usuario = Usuario.objects.create(**usuario_data)
            
            # Devolver datos del personal creado
            return Response({
                'mensaje': 'Personal creado exitosamente',
                'personal': serializer.data,
                'usuario': {
                    'id': usuario.id,
                    'rol': usuario.rol,
                    'estado': usuario.estado
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## CREAR CLIENTE
class ClienteCreateView(APIView):
    permission_classes = [ IsAdminUser ]
    
    def post(self, request):
        serializer = ClienteCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Crear el cliente
            cliente = serializer.save()
            
            # Verificar si se debe crear un usuario
            crear_usuario = request.data.get('crear_usuario', False)
            usuario = None
            
            if crear_usuario:
                # Crear usuario asociado al cliente
                usuario_data = {
                    'password': make_password('cliente123'),  # Contraseña temporal
                    'rol': 'cliente',  # Rol por defecto para clientes
                    'estado': 'activo',
                    'cliente': cliente
                }
                
                usuario = Usuario.objects.create(**usuario_data)
            
            # Devolver datos del cliente creado
            response_data = {
                'mensaje': 'Cliente creado exitosamente',
                'cliente': serializer.data
            }
            
            if usuario:
                response_data['usuario'] = {
                    'id': usuario.id,
                    'rol': usuario.rol,
                    'estado': usuario.estado
                }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


## CREATE USUARIO
class UsuarioCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = UsuarioCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Encriptar la contraseña antes de guardar
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            
            usuario = serializer.save()
            return Response(UsuarioSerializer(usuario).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



## *********************************************************************************************
## READ VIEWS:

## GET USUARIOS
class UsuarioListView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

