from django.db import models
from apps.usuarios.models import Cliente, Usuario
from apps.productos.models import Producto



class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    fecha = models.DateTimeField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)  # Enum: 'completada', 'cancelada', 'pendiente'
    creado_por_voz = models.BooleanField(blank=True, null=True)
    stripe_transaction_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'venta'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, models.DO_NOTHING)
    producto = models.ForeignKey(Producto, models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fue_recomendacion = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'detalleventa'


class ComandoVoz(models.Model):
    comando = models.CharField(unique=True, max_length=255)
    accion = models.CharField(max_length=100)
    parametros = models.TextField(blank=True, null=True)  # JSON con parámetros
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'comandovoz'

