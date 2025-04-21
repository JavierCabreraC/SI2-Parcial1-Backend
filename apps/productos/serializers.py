from rest_framework import serializers
from .models import Categoria, Producto



class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [
            'id', 'nombre', 'precio', 'stock_actual', 'stock_minimo',
            'categoria', 'imagen_url', 'activo', 'fecha_creacion',
            'fecha_modificacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']


class ProductoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'stock_actual', 'categoria', 'activo']