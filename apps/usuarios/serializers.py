# apps/usuarios/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers
from .models import Usuario, Cliente, Personal



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs['username'] = attrs.get('email')
        if not attrs['username']:
            raise serializers.ValidationError("El email es requerido")
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añadir claims personalizados al token
        token['rol'] = user.rol
        # Puedes añadir más información si lo necesitas
        # token['name'] = user.username

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_completo', 'numero_ci', 'telefono', 'direccion', 'email', 
                 'puntos_acumulados', 'descuentos_disponibles', 'descuentos_utilizados']


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ['id', 'nombre_completo', 'numero_ci', 'telefono', 'direccion', 'email', 
                 'fecha_contratacion']


class UsuarioSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(required=False)
    personal = PersonalSerializer(required=False)

    class Meta:
        model = Usuario
        fields = ['id', 'rol', 'estado', 'fecha_creacion', 'cliente', 'personal']
        read_only_fields = ['id', 'fecha_creacion']


class UsuarioSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'rol', 'estado', 'fecha_creacion']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(required=False)
    personal = PersonalSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'rol', 'estado', 'password', 'cliente', 'personal']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        cliente_data = validated_data.pop('cliente', None)
        personal_data = validated_data.pop('personal', None)
        
        usuario = Usuario.objects.create(**validated_data)
        
        if cliente_data:
            cliente = Cliente.objects.create(**cliente_data)
            usuario.cliente = cliente
            
        if personal_data:
            personal = Personal.objects.create(**personal_data)
            usuario.personal = personal
            
        usuario.save()
        return usuario


class PersonalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ['nombre_completo', 'numero_ci', 'telefono', 'direccion', 'email', 'fecha_contratacion']

    def validate_email(self, value):
        if Personal.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso por otro personal.")
        return value


class ClienteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'numero_ci', 'telefono', 'direccion', 'email']

    def validate_email(self, value):
        if value and Cliente.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está en uso por otro cliente.")
        return value

