from rest_framework import generics, status
from rest_framework.response import Response
from django.utils import timezone
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer
from apps.usuarios.permissions import IsAlmacenista
from apps.usuarios.utils import registrar_accion



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


## *********************

class ProductoDetailView(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de un producto específico.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAlmacenista]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'LeerProducto', ip)
        
        return Response(serializer.data)


class ProductoUpdateView(generics.UpdateAPIView):
    """
    Vista para actualizar la información de un producto existente.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAlmacenista]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Actualizar la fecha de modificación
        producto = serializer.save(fecha_modificacion=timezone.now())
        
        # Verificar si el stock está por debajo del mínimo después de la actualización
        if producto.stock_actual < producto.stock_minimo:
            # Crear notificación de alerta de stock
            Notificacion.objects.create(
                usuario=request.user,
                mensaje=f"El producto {producto.nombre} está bajo el stock mínimo ({producto.stock_actual}/{producto.stock_minimo})",
                tipo='alerta_stock'
            )
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'ActualizarProducto', ip)
        
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ProductoDeleteView(generics.DestroyAPIView):
    """
    Vista para eliminar un producto del catálogo.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAlmacenista]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Guardar el nombre para incluirlo en la respuesta
        nombre_producto = instance.nombre
        
        # Realizar eliminación lógica en lugar de física
        instance.activo = False
        instance.fecha_modificacion = timezone.now()
        instance.save()
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'EliminarProducto', ip)
        
        return Response({
            "mensaje": f"El producto '{nombre_producto}' ha sido eliminado correctamente.",
            "id": instance.id
        }, status=status.HTTP_200_OK)
