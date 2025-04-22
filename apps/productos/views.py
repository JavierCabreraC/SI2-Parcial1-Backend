from rest_framework import generics, status
from rest_framework.response import Response
from django.db import connection
from rest_framework.views import APIView
from django.utils import timezone
from apps.usuarios.models import Notificacion
from apps.usuarios.views import get_client_ip
from .models import Categoria, Producto
from .serializers import CategoriaSerializer, ProductoSerializer, ProductoSimpleSerializer
from apps.usuarios.permissions import IsAlmacenista
from apps.usuarios.utils import registrar_accion
from apps.productos import models



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
        registrar_accion(request.user.id, 'ConsultarCategoria', ip)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductoListView(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSimpleSerializer  # Cambiar al nuevo serializer
    permission_classes = [IsAlmacenista]


class ProductoCreateView(generics.CreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [ IsAlmacenista ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'LeerProducto', ip)
        
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


## ******************************************

class CategoriaDetailView(generics.RetrieveAPIView):
    """
    Vista para obtener los detalles de una categoría específica.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAlmacenista]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'ConsultarCategoria', ip)
        
        return Response(serializer.data)


class CategoriaUpdateView(generics.UpdateAPIView):
    """
    Vista para actualizar la información de una categoría existente.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAlmacenista]
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # No actualizamos fecha_creacion, solo guardamos los cambios
        serializer.save()
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'ActualizarCategoria', ip)
        
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CategoriaDeleteView(generics.DestroyAPIView):
    """
    Vista para eliminar una categoría.
    Comprueba si hay productos asociados antes de eliminar.
    """
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAlmacenista]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Verificar si hay productos asociados a esta categoría
        productos_asociados = Producto.objects.filter(categoria=instance).count()
        
        if productos_asociados > 0:
            return Response({
                "error": f"No se puede eliminar la categoría. Tiene {productos_asociados} productos asociados.",
                "mensaje": "Debe reasignar o eliminar los productos antes de eliminar la categoría."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Guardar el nombre para incluirlo en la respuesta
        nombre_categoria = instance.nombre
        
        # Realizar la eliminación
        instance.delete()
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'ActualizarCategoria', ip)
        
        return Response({
            "mensaje": f"La categoría '{nombre_categoria}' ha sido eliminada correctamente.",
            "id": instance.id
        }, status=status.HTTP_200_OK)


## Vista adicional para listar productos por categoría
class ProductoPorCategoriaView(generics.ListAPIView):
    """
    Vista para listar todos los productos de una categoría específica.
    """
    serializer_class = ProductoSerializer
    permission_classes = [IsAlmacenista]
    
    def get_queryset(self):
        categoria_id = self.kwargs['categoria_id']
        return Producto.objects.filter(categoria_id=categoria_id, activo=True)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Si no hay productos en esta categoría
        if not queryset.exists():
            try:
                # Verificar si la categoría existe
                categoria = Categoria.objects.get(pk=self.kwargs['categoria_id'])
                return Response({
                    "mensaje": f"No hay productos activos en la categoría '{categoria.nombre}'.",
                    "categoria_id": categoria.id,
                    "productos": []
                })
            except Categoria.DoesNotExist:
                return Response({
                    "error": "La categoría especificada no existe."
                }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        
        # Registrar acción en bitácora
        ip = get_client_ip(request)
        registrar_accion(request.user.id, 'LeerProducto', ip)
        
        return Response(serializer.data)


class ReporteBajoStockView(APIView):
    """
    Vista para generar un reporte de productos con bajo stock utilizando SQL puro.
    """
    permission_classes = [IsAlmacenista]

    def get(self, request):
        # Obtener el parámetro opcional de categoría
        categoria_id = request.query_params.get('categoria_id', None)

        # Construir la consulta SQL
        sql = """
            SELECT 
                p.id, 
                p.nombre, 
                p.stock_actual, 
                p.stock_minimo, 
                c.nombre AS categoria
            FROM Producto p
            LEFT JOIN Categoria c ON p.categoria_id = c.id
            WHERE p.stock_actual < p.stock_minimo AND p.activo = TRUE
        """
        params = []

        # Agregar filtro por categoría si se especifica
        if categoria_id:
            sql += " AND p.categoria_id = %s"
            params.append(categoria_id)

        # Ejecutar la consulta
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()

        # Formatear los resultados
        productos = [
            {
                "id": row[0],
                "nombre": row[1],
                "stock_actual": row[2],
                "stock_minimo": row[3],
                "categoria": row[4],
            }
            for row in rows
        ]

        # Si no hay productos con bajo stock
        if not productos:
            return Response({"mensaje": "No hay productos con bajo stock."}, status=200)

        return Response(productos, status=200)

