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
    class RolChoices(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CLIENTE = 'cliente', 'Cliente'
        ALMACENISTA = 'almacenista', 'Almacenista'

    class EstadoChoices(models.TextChoices):
        ACTIVO = 'activo', 'Activo'
        INACTIVO = 'inactivo', 'Inactivo'

    password = models.CharField(max_length=255)
    rol = models.CharField(
        max_length=20,
        choices=RolChoices.choices,
        default=RolChoices.CLIENTE
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoChoices.choices,
        default=EstadoChoices.ACTIVO
    )
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    cliente = models.OneToOneField(
        'Cliente',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    personal = models.OneToOneField(
        'Personal',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'usuario'


class TipoAccionBitacora(models.Model):
    class AccionChoices(models.TextChoices):
        LOGIN = 'Login', 'Login'
        LOGOUT = 'Logout', 'Logout'
        CREAR_PRODUCTO = 'CrearProducto', 'Crear Producto'
        ACTUALIZAR_PRODUCTO = 'ActualizarProducto', 'Actualizar Producto'
        CREAR_VENTA = 'CrearVenta', 'Crear Venta'
        CANCELAR_VENTA = 'CancelarVenta', 'Cancelar Venta'
        ACTUALIZAR_STOCK = 'ActualizarStock', 'Actualizar Stock'
        CREAR_CLIENTE = 'CrearCliente', 'Crear Cliente'
        ACTUALIZAR_CLIENTE = 'ActualizarCliente', 'Actualizar Cliente'
        CREAR_CATEGORIA = 'CrearCategoria', 'Crear Categoría'
        GENERAR_REPORTE = 'GenerarReporte', 'Generar Reporte'
        # Nuevas acciones
        LEER_PRODUCTO = 'ConsultarProducto', 'Consultar Producto'
        LEER_CLIENTE = 'ConsultarCliente', 'Consultar Cliente'
        LEER_USUARIOS = 'ConsultarUsuarios', 'Consultar Usuarios'
        LEER_CATEGORIA = 'ConsultarCategoria', 'Consultar Categoria'
        ACTUALIZAR_CATEGORIA = 'ActualizarCategoria', 'Actualizar Categoría'
        CREAR_PERSONAL = 'CrearPersonal', 'Crear Personal'
        LEER_PERSONAL = 'ConsultarPersonal', 'Consultar Personal'
        ACTUALIZAR_PERSONAL = 'ActualizarPersonal', 'Actualizar Personal'
        LEER_VENTA = 'ConsultarVenta', 'Consultar Venta'
        LEER_HISTORIAL = 'ConsultarHistorial', 'Consultar Historial'
        CREAR_NOTIFICACION = 'CrearNotificacion', 'Crear Notificacion'
        LEER_NOTIFICACION = 'ConsultarNotificacion', 'Consultar Notificacion'
        ACTUALIZAR_NOTIFICACION = 'ActualizarNotificacion', 'Actualizar Notificacion'
        CREAR_COMANDOS = 'CrearComandos', 'Crear Comandos'	
        LEER_COMANDOS = 'ConsultarComandos', 'Consultar Comandos'


    accion = models.CharField(
        max_length=50,
        choices=AccionChoices.choices
    )

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
    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE  # Refleja ON DELETE CASCADE
    )
    termino_busqueda = models.CharField(
        max_length=255  # Refleja VARCHAR(255) NOT NULL
    )
    fecha = models.DateTimeField(
        auto_now_add=True  # Refleja DEFAULT CURRENT_TIMESTAMP
    )
    convertida_venta = models.BooleanField(
        default=False  # Refleja DEFAULT FALSE
    )

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

