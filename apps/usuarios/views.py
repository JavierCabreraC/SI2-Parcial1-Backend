from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario, Cliente, Personal
from .utils import generate_jwt_token
from .serializers import UsuarioSerializer, UsuarioCreateSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser



@api_view(['POST'])
@permission_classes([AllowAny])  # Permitir acceso sin autenticación
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

        # Generar el token JWT
        token = generate_jwt_token(usuario.id, usuario.rol)

        return Response({
            "access_token": token,
            "rol": usuario.rol
        }, status=status.HTTP_200_OK)

    except Usuario.DoesNotExist:
        return Response({"error": "El correo ingresado no tiene un usuario asociado"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class UsuarioListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data)

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

