# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# Este archivo no irá a main

from django.db import models


class Bitacora(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    tipo_accion = models.ForeignKey('Tipoaccionbitacora', models.DO_NOTHING)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    ip_direccion = models.GenericIPAddressField()

    class Meta:
        managed = False
        db_table = 'bitacora'


class Categoria(models.Model):
    nombre = models.CharField(unique=True, max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categoria'


class Cliente(models.Model):
    nombre_completo = models.CharField(max_length=50)
    numero_ci = models.IntegerField()
    telefono = models.CharField(max_length=14, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50, blank=True, null=True)
    puntos_acumulados = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    descuentos_disponibles = models.IntegerField(blank=True, null=True)
    descuentos_utilizados = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cliente'


class Comandovoz(models.Model):
    comando = models.CharField(unique=True, max_length=255)
    accion = models.CharField(max_length=100)
    parametros = models.TextField(blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comandovoz'


class Detalleventa(models.Model):
    venta = models.ForeignKey('Venta', models.DO_NOTHING)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    fue_recomendacion = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalleventa'


class Historialbusqueda(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    termino_busqueda = models.CharField(max_length=255)
    fecha = models.DateTimeField(blank=True, null=True)
    convertida_venta = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historialbusqueda'


class Notificacion(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    mensaje = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    leido = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificacion'


class Personal(models.Model):
    nombre_completo = models.CharField(max_length=50)
    numero_ci = models.IntegerField()
    telefono = models.CharField(max_length=14)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50)
    fecha_contratacion = models.DateField()

    class Meta:
        managed = False
        db_table = 'personal'


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock_actual = models.IntegerField()
    stock_minimo = models.IntegerField()
    categoria = models.ForeignKey(Categoria, models.DO_NOTHING, blank=True, null=True)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'


class Productorecomendacion(models.Model):
    producto_base = models.ForeignKey(Producto, models.DO_NOTHING)
    producto_recomendado = models.ForeignKey(Producto, models.DO_NOTHING, related_name='productorecomendacion_producto_recomendado_set')
    score = models.DecimalField(max_digits=5, decimal_places=4)
    frecuencia = models.IntegerField()
    ultima_actualizacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productorecomendacion'
        unique_together = (('producto_base', 'producto_recomendado'),)


class Tipoaccionbitacora(models.Model):
    accion = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'tipoaccionbitacora'


class Usuario(models.Model):
    password = models.CharField(max_length=255)
    rol = models.TextField()  # This field type is a guess.
    estado = models.TextField()  # This field type is a guess.
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    cliente = models.OneToOneField(Cliente, models.DO_NOTHING, blank=True, null=True)
    personal = models.OneToOneField(Personal, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'


class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING)
    fecha = models.DateTimeField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    creado_por_voz = models.BooleanField(blank=True, null=True)
    stripe_transaction_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(unique=True, max_length=255, blank=True, null=True)
    stripe_payment_status = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'venta'
