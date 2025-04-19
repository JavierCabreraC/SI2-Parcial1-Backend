from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer
from apps.usuarios.permissions import IsAlmacenista



# Create your views here.
class CategoriaListView(generics.ListAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [ IsAlmacenista ]


class CategoriaCreateView(generics.CreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [ IsAlmacenista ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Establecer la fecha de creación antes de guardar
        categoria = serializer.save(fecha_creacion=timezone.now())

        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'LeerCliente', ip)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [ IsAlmacenista ]


class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [ IsAlmacenista ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Establecer valores por defecto
        producto = serializer.save(
            fecha_creacion=timezone.now(),
            fecha_modificacion=timezone.now(),
            activo=True
        )
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

