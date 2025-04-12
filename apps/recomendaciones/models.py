from django.db import models
from apps.productos.models import Producto



class ProductoRecomendacion(models.Model):
    producto_base = models.ForeignKey(Producto, models.DO_NOTHING)
    producto_recomendado = models.ForeignKey(Producto, models.DO_NOTHING, related_name='productorecomendacion_producto_recomendado_set')
    score = models.DecimalField(max_digits=5, decimal_places=4)
    frecuencia = models.IntegerField()
    ultima_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'productorecomendacion'
        unique_together = (('producto_base', 'producto_recomendado'),)


