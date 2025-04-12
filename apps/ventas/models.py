from django.db import models
from apps.usuarios.models import Cliente, Usuario
from apps.productos.models import Producto
from apps.ventas.models import Venta



class Venta(models.Model):
    class EstadoChoices(models.TextChoices):
        COMPLETADA = 'completada', 'Completada'
        CANCELADA = 'cancelada', 'Cancelada'
        PENDIENTE = 'pendiente', 'Pendiente'

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT,  # Refleja ON DELETE RESTRICT
        blank=True,
        null=True
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.RESTRICT  # Refleja ON DELETE RESTRICT
    )
    fecha = models.DateTimeField(
        auto_now_add=True  # Refleja DEFAULT CURRENT_TIMESTAMP
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,  # Refleja DEFAULT 0
        validators=[
            models.validators.MinValueValidator(0)
        ]  # Refleja CHECK (subtotal >= 0)
    )
    descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,  # Refleja DEFAULT 0
        validators=[
            models.validators.MinValueValidator(0)
        ]  # Refleja CHECK (descuento >= 0)
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,  # Refleja DEFAULT 0
        validators=[
            models.validators.MinValueValidator(0)
        ]  # Refleja CHECK (total >= 0)
    )
    estado = models.CharField(
        max_length=50,
        choices=EstadoChoices.choices,
        default=EstadoChoices.COMPLETADA  # Refleja DEFAULT 'completada'
    )
    creado_por_voz = models.BooleanField(
        default=False  # Refleja DEFAULT FALSE
    )
    stripe_transaction_id = models.CharField(
        unique=True,
        max_length=255,
        blank=True,
        null=True
    )
    stripe_payment_intent_id = models.CharField(
        unique=True,
        max_length=255,
        blank=True,
        null=True
    )
    stripe_payment_status = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'venta'


class DetalleVenta(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE  # Refleja ON DELETE CASCADE
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT  # Refleja ON DELETE RESTRICT
    )
    cantidad = models.IntegerField(
        validators=[
            models.validators.MinValueValidator(1)
        ]  # Refleja CHECK (cantidad > 0)
    )
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            models.validators.MinValueValidator(0)
        ]  # Refleja CHECK (precio_unitario >= 0)
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            models.validators.MinValueValidator(0)
        ]  # Refleja CHECK (subtotal >= 0)
    )
    fue_recomendacion = models.BooleanField(
        default=False  # Refleja DEFAULT FALSE
    )

    class Meta:
        db_table = 'detalleventa'


class ComandoVoz(models.Model):
    comando = models.CharField(unique=True, max_length=255)
    accion = models.CharField(max_length=100)
    parametros = models.TextField(blank=True, null=True)  # JSON con parámetros
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'comandovoz'
