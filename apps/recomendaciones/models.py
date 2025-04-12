from django.db import models
from apps.productos.models import Producto
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator



class ProductoRecomendacion(models.Model):
    producto_base = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,  # Refleja ON DELETE CASCADE
        related_name='recomendaciones_base'
    )
    producto_recomendado = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,  # Refleja ON DELETE CASCADE
        related_name='recomendaciones_recomendado'
    )
    score = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ]  # Refleja CHECK (score BETWEEN 0 AND 1)
    )
    frecuencia = models.IntegerField(
        default=1,  # Refleja DEFAULT 1
        validators=[
            MinValueValidator(1)
        ]  # Refleja CHECK (frecuencia > 0)
    )
    ultima_actualizacion = models.DateTimeField(
        auto_now=True  # Refleja DEFAULT CURRENT_TIMESTAMP
    )

    class Meta:
        db_table = 'productorecomendacion'
        unique_together = (('producto_base', 'producto_recomendado'),)  # Refleja UNIQUE
        constraints = [
            models.CheckConstraint(
                check=~models.Q(producto_base=models.F('producto_recomendado')),
                name='different_products'  # Refleja CHECK (producto_base_id != producto_recomendado_id)
            )
        ]
