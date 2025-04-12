-- Creación de tablas para el Sistema POS con IA

-- Tabla de Usuarios
-- CREATE TABLE Usuario (
--     id SERIAL PRIMARY KEY,
--     username VARCHAR(100) NOT NULL UNIQUE,
--     password VARCHAR(255) NOT NULL,
--     email VARCHAR(100) NOT NULL UNIQUE,
--     role VARCHAR(50) NOT NULL CHECK (role IN ('admin', 'vendedor', 'almacenista')),
--     is_active BOOLEAN DEFAULT TRUE,
--     fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     ultimo_acceso TIMESTAMP
-- );

CREATE TABLE "cliente" (
    "ClienteID" SMALLSERIAL NOT NULL,
    "NombreCompleto" VARCHAR(60) NOT NULL,
    "Telefono" VARCHAR(30) NOT NULL,
    "NumeroCI" INTEGER NOT NULL,
    "Direccion" VARCHAR(100),
    "Email" VARCHAR(50) NOT NULL,
    "UltimaCompra" TIMESTAMP
    CONSTRAINT "cliente_pkey" PRIMARY KEY ("ClienteID")
);

CREATE TABLE "personal" (
    "PersonalID" SMALLSERIAL NOT NULL,
    "NombreCompleto" VARCHAR(60) NOT NULL,
    "NumeroCI" INTEGER NOT NULL,
    "Telefono" VARCHAR(30) NOT NULL,
    "Direccion" VARCHAR(100) NOT NULL,
    "Activo" BOOLEAN NOT NULL DEFAULT true,
    "Email" VARCHAR(50) NOT NULL,
    "CargoID" SMALLINT NOT NULL,
    CONSTRAINT "personal_pkey" PRIMARY KEY ("PersonalID")
);

CREATE TABLE "usuario" (
    "UsuarioID" SMALLSERIAL NOT NULL,
    "Rol" "usuario_Rol" NOT NULL DEFAULT 'Almacenero',
    "Estado" "usuario_Estado" NOT NULL DEFAULT 'Activo',
    "PasswrdHash" VARCHAR(256) NOT NULL,
    "CreatedAt" TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP(0) DEFAULT CURRENT_TIMESTAMP,
    "PersonalID" SMALLINT,
    "ClienteID" SMALLINT,
    CONSTRAINT "usuario_pkey" PRIMARY KEY ("UsuarioID")
);

-- Tabla de Categorías
CREATE TABLE Categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE Producto (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
    categoria_id INT REFERENCES Categoria(id) ON DELETE SET NULL,
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- -- Tabla de Clientes
-- CREATE TABLE Cliente (
--     id SERIAL PRIMARY KEY,
--     nombre VARCHAR(100) NOT NULL,
--     apellido VARCHAR(100) NOT NULL,
--     email VARCHAR(100) UNIQUE,
--     telefono VARCHAR(20),
--     direccion TEXT,
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     ultima_compra TIMESTAMP
-- );

-- Tabla de Ventas
CREATE TABLE Venta (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES Cliente(ClienteID) ON DELETE RESTRICT,
    usuario_id INT NOT NULL REFERENCES Usuario(UsuarioID) ON DELETE RESTRICT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (subtotal >= 0),
    descuento DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (descuento >= 0),
    impuesto DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (impuesto >= 0),
    total DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    tipo_pago VARCHAR(50) NOT NULL CHECK (tipo_pago IN ('efectivo', 'tarjeta_credito', 'tarjeta_debito', 'transferencia', 'otro')),
    estado VARCHAR(50) NOT NULL DEFAULT 'completada' CHECK (estado IN ('completada', 'cancelada', 'pendiente')),
    creado_por_voz BOOLEAN DEFAULT FALSE
);

-- Tabla de Detalles de Venta
CREATE TABLE DetalleVenta (
    id SERIAL PRIMARY KEY,
    venta_id INT NOT NULL REFERENCES Venta(id) ON DELETE CASCADE,
    producto_id INT NOT NULL REFERENCES Producto(id) ON DELETE RESTRICT,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
    subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
    fue_recomendacion BOOLEAN DEFAULT FALSE
);

-- Tabla de Notificaciones
CREATE TABLE Notificacion (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES Usuario(id) ON DELETE CASCADE,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'sistema' CHECK (tipo IN ('alerta_stock', 'sistema', 'venta', 'otro')),
    leido BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_lectura TIMESTAMP
);

-- Tabla de Recomendaciones de Productos
CREATE TABLE ProductoRecomendacion (
    id SERIAL PRIMARY KEY,
    producto_base_id INT NOT NULL REFERENCES Producto(id) ON DELETE CASCADE,
    producto_recomendado_id INT NOT NULL REFERENCES Producto(id) ON DELETE CASCADE,
    score DECIMAL(5,4) NOT NULL CHECK (score BETWEEN 0 AND 1),
    frecuencia INT NOT NULL DEFAULT 1 CHECK (frecuencia > 0),
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_recomendacion UNIQUE (producto_base_id, producto_recomendado_id),
    CONSTRAINT different_products CHECK (producto_base_id != producto_recomendado_id)
);

-- Tabla de Comandos de Voz
CREATE TABLE ComandoVoz (
    id SERIAL PRIMARY KEY,
    comando VARCHAR(255) NOT NULL UNIQUE,
    accion VARCHAR(100) NOT NULL,
    parametros TEXT, -- Almacenará JSON
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de Historial de Búsquedas
CREATE TABLE HistorialBusqueda (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES Cliente(id) ON DELETE CASCADE,
    termino_busqueda VARCHAR(255) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    convertida_venta BOOLEAN DEFAULT FALSE
);

-- Creación de índices para optimizar consultas frecuentes
CREATE INDEX idx_producto_codigo ON Producto(codigo);
CREATE INDEX idx_producto_nombre ON Producto(nombre);
CREATE INDEX idx_venta_fecha ON Venta(fecha);
CREATE INDEX idx_venta_cliente ON Venta(cliente_id);
CREATE INDEX idx_detalleventa_producto ON DetalleVenta(producto_id);
CREATE INDEX idx_productorec_base ON ProductoRecomendacion(producto_base_id);
CREATE INDEX idx_producto_stock ON Producto(stock_actual);

-- Función y trigger para notificar stock bajo
CREATE OR REPLACE FUNCTION notificar_stock_bajo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.stock_actual <= NEW.stock_minimo AND OLD.stock_actual > OLD.stock_minimo THEN
        INSERT INTO Notificacion (usuario_id, mensaje, tipo)
        SELECT id, 'El producto ' || NEW.nombre || ' (Código: ' || NEW.codigo || ') está bajo en stock (' || NEW.stock_actual || ' unidades).', 'alerta_stock'
        FROM Usuario
        WHERE role = 'almacenista' AND is_active = TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_stock_bajo
AFTER UPDATE OF stock_actual ON Producto
FOR EACH ROW
EXECUTE FUNCTION notificar_stock_bajo();

-- Función y trigger para actualizar stock después de una venta
CREATE OR REPLACE FUNCTION actualizar_stock_producto()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Producto
    SET stock_actual = stock_actual - NEW.cantidad
    WHERE id = NEW.producto_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_stock
AFTER INSERT ON DetalleVenta
FOR EACH ROW
EXECUTE FUNCTION actualizar_stock_producto();

-- Función y trigger para actualizar la fecha de última compra del cliente
CREATE OR REPLACE FUNCTION actualizar_ultima_compra()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.cliente_id IS NOT NULL THEN
        UPDATE Cliente
        SET ultima_compra = NEW.fecha
        WHERE id = NEW.cliente_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_ultima_compra
AFTER INSERT ON Venta
FOR EACH ROW
EXECUTE FUNCTION actualizar_ultima_compra();

-- Función y trigger para actualizar la fecha de modificación del producto
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion_producto()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_fecha_modificacion
BEFORE UPDATE ON Producto
FOR EACH ROW
EXECUTE FUNCTION actualizar_fecha_modificacion_producto();

-- Inserts iniciales para pruebas (opcional)

-- Insertar categorías iniciales
INSERT INTO Categoria (nombre, descripcion) VALUES 
('Smartphones', 'Teléfonos inteligentes de diversas marcas'),
('Laptops', 'Computadoras portátiles'),
('Accesorios', 'Accesorios para dispositivos electrónicos'),
('Tablets', 'Tablets de diversas marcas'),
('Audio', 'Dispositivos de audio y sonido');

-- Insertar usuario administrador
INSERT INTO Usuario (username, password, email, role) VALUES 
('admin', 'pbkdf2_sha256$260000$q9BH6JhvZlDnJVBu$q8V+2dzxQZUzjqyX3fO+GmUuwhv4QUUZyOV1p3z0Xg8=', 'admin@example.com', 'admin');

-- Insertar comandos de voz iniciales
INSERT INTO ComandoVoz (comando, accion, parametros) VALUES 
('agregar producto', 'add_to_cart', '{"requires_product_id": true}'),
('eliminar producto', 'remove_from_cart', '{"requires_product_id": true}'),
('calcular total', 'calculate_total', '{}'),
('aplicar descuento', 'apply_discount', '{"requires_amount": true}'),
('finalizar venta', 'complete_sale', '{}'),
('buscar producto', 'search_product', '{"requires_term": true}');
