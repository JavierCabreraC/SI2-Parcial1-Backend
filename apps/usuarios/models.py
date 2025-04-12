from django.db import models



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
        db_table = 'cliente'


class Personal(models.Model):
    nombre_completo = models.CharField(max_length=50)
    numero_ci = models.IntegerField()
    telefono = models.CharField(max_length=14)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=50)
    fecha_contratacion = models.DateField()

    class Meta:
        db_table = 'personal'


class Usuario(models.Model):
    password = models.CharField(max_length=255)
    rol = models.TextField()  # Enum: 'admin', 'cliente', 'almacenista'
    estado = models.TextField()  # Enum: 'activo', 'inactivo'
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    cliente = models.OneToOneField(Cliente, models.DO_NOTHING, blank=True, null=True)
    personal = models.OneToOneField(Personal, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'usuario'


class TipoAccionBitacora(models.Model):
    accion = models.TextField()  # Enum: 'Login', 'Logout', etc.

    class Meta:
        db_table = 'tipoaccionbitacora'


class Bitacora(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.RESTRICT)
    tipo_accion = models.ForeignKey('TipoAccionBitacora', on_delete=models.RESTRICT)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    ip_direccion = models.GenericIPAddressField()

    class Meta:
        db_table = 'bitacora'


class HistorialBusqueda(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    termino_busqueda = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
    convertida_venta = models.BooleanField(default=False)

    class Meta:
        db_table = 'historialbusqueda'


class Notificacion(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=100)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('alerta_stock', 'Alerta de Stock'),
            ('sistema', 'Sistema'),
            ('venta', 'Venta'),
        ],
        default='sistema',
    )
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'notificacion'

