-- Base de datos creada en Neon:

CREATE TYPE usuario_rol AS ENUM ('admin', 'cliente', 'almacenista');

CREATE TYPE usuario_estado AS ENUM ('activo', 'inactivo');

CREATE TYPE accion_bitacora AS ENUM (
    'Login', 'Logout', 'CrearProducto', 'ActualizarProducto', 
    'CrearVenta', 'CancelarVenta', 'ActualizarStock',
    'CrearCliente', 'ActualizarCliente', 'CrearCategoria', 'GenerarReporte'
    -- Añadir más según necesidad
);

-- Tabla de Personal (nueva)
CREATE TABLE Personal (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(50) NOT NULL,
    numero_ci INTEGER NOT NULL,
    telefono VARCHAR(14) NOT NULL,
    direccion VARCHAR(50),
    email VARCHAR(50) NOT NULL UNIQUE,
    fecha_contratacion DATE NOT NULL
);

-- Tabla de Clientes
CREATE TABLE Cliente (
    id SERIAL PRIMARY KEY,
    nombre_completo VARCHAR(50) NOT NULL,
    numero_ci INTEGER NOT NULL,
    telefono VARCHAR(14),
    direccion VARCHAR(50),
    email VARCHAR(50) UNIQUE
);

ALTER TABLE Cliente
    ADD COLUMN puntos_acumulados DECIMAL(6,2) DEFAULT 0,
    ADD COLUMN descuentos_disponibles INT DEFAULT 0,
    ADD COLUMN descuentos_utilizados INT DEFAULT 0;

-- Tabla de Usuarios
CREATE TABLE Usuario (
    id SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    rol usuario_rol NOT NULL,
    estado usuario_estado NOT NULL DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cliente_id INT UNIQUE REFERENCES Cliente(id) ON DELETE SET NULL,
    personal_id INT UNIQUE REFERENCES Personal(id) ON DELETE SET NULL,
    CONSTRAINT usuario_unico CHECK (
        (cliente_id IS NOT NULL AND personal_id IS NULL) OR
        (cliente_id IS NULL AND personal_id IS NOT NULL)
    )
);

CREATE TABLE TipoAccionBitacora (
    id SERIAL PRIMARY KEY,
    accion accion_bitacora NOT NULL
);

-- Tabla de Bitácora
CREATE TABLE Bitacora (
    id SERIAL PRIMARY KEY,
    usuario_id INT NOT NULL REFERENCES Usuario(id) ON DELETE RESTRICT,
    tipo_accion_id INT NOT NULL REFERENCES TipoAccionBitacora(id) ON DELETE RESTRICT,
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_direccion INET NOT NULL
);

-- Tabla de Categorías
CREATE TABLE Categoria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(100),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE Producto (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
    categoria_id INT REFERENCES Categoria(id) ON DELETE SET NULL,
    imagen_url VARCHAR(255),
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Ventas
CREATE TABLE Venta (
    id SERIAL PRIMARY KEY,
    cliente_id INT REFERENCES Cliente(id) ON DELETE RESTRICT,
    usuario_id INT NOT NULL REFERENCES Usuario(id) ON DELETE RESTRICT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (subtotal >= 0),
    descuento DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (descuento >= 0),
    total DECIMAL(10,2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    estado VARCHAR(50) NOT NULL DEFAULT 'completada' CHECK (estado IN ('completada', 'cancelada', 'pendiente')),
    creado_por_voz BOOLEAN DEFAULT FALSE
);

ALTER TABLE Venta
    ADD COLUMN stripe_transaction_id VARCHAR(255) UNIQUE,
    ADD COLUMN stripe_payment_intent_id VARCHAR(255) UNIQUE,
    ADD COLUMN stripe_payment_status VARCHAR(50);

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
    mensaje VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL DEFAULT 'sistema' CHECK (tipo IN ('alerta_stock', 'sistema', 'venta')),
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

CREATE INDEX idx_producto_nombre ON Producto(nombre);
CREATE INDEX idx_venta_fecha ON Venta(fecha);
CREATE INDEX idx_venta_cliente ON Venta(cliente_id);
CREATE INDEX idx_detalleventa_producto ON DetalleVenta(producto_id);
CREATE INDEX idx_productorec_base ON ProductoRecomendacion(producto_base_id);
CREATE INDEX idx_producto_stock ON Producto(stock_actual);
CREATE INDEX idx_bitacora_usuario ON Bitacora(usuario_id);
CREATE INDEX idx_bitacora_tipo_accion ON Bitacora(tipo_accion_id);
CREATE INDEX idx_usuario_cliente ON Usuario(cliente_id);
CREATE INDEX idx_usuario_personal ON Usuario(personal_id);


-- ************************************************************************************************
-- ************************************************************************************************
-- ************************************************************************************************


ALTER TYPE accion_bitacora ADD VALUE 'LeerPersonal';
ALTER TYPE accion_bitacora ADD VALUE 'LeerCliente';
ALTER TYPE accion_bitacora ADD VALUE 'LeerUsuario';


ALTER TYPE accion_bitacora ADD VALUE 'ConsultarCategoria';
ALTER TYPE accion_bitacora ADD VALUE 'ActualizarCategoria';
ALTER TYPE accion_bitacora ADD VALUE 'CrearPersonal';
-- ALTER TYPE accion_bitacora ADD VALUE 'ConsultarPersonal'; ## repetido
ALTER TYPE accion_bitacora ADD VALUE 'ActualizarPersonal';
ALTER TYPE accion_bitacora ADD VALUE 'ConsultarVenta';
ALTER TYPE accion_bitacora ADD VALUE 'ConsultarHistorial';
ALTER TYPE accion_bitacora ADD VALUE 'CrearNotificacion';
ALTER TYPE accion_bitacora ADD VALUE 'ConsultarNotificacion';
ALTER TYPE accion_bitacora ADD VALUE 'ActualizarNotificacion';
ALTER TYPE accion_bitacora ADD VALUE 'CrearComandos';
ALTER TYPE accion_bitacora ADD VALUE 'ConsultarComandos';


INSERT INTO TipoAccionBitacora (accion) VALUES 
    ('ConsultarCategoria'),
    ('ActualizarCategoria'),
    ('CrearPersonal'),
    ('ConsultarPersonal'),
    ('ActualizarPersonal'),
    ('ConsultarVenta'),
    ('ConsultarHistorial'),
    ('CrearNotificacion'),
    ('ConsultarNotificacion'),
    ('ActualizarNotificacion'),
    ('CrearComandos'),
    ('ConsultarComandos');


ALTER TYPE accion_bitacora ADD VALUE 'LeerProducto';
INSERT INTO TipoAccionBitacora(accion) VALUES ('LeerProducto');


ALTER TYPE accion_bitacora ADD VALUE 'EliminarProducto';
INSERT INTO TipoAccionBitacora(accion) VALUES ('EliminarProducto');




-- Inserción de Productos
INSERT INTO Producto (nombre, precio, stock_actual, stock_minimo, categoria_id, activo)
VALUES
    -- Categoría 1: Computadoras
    ('Laptop HP Pavilion 15.6"', 3799.99, 15, 3, 3, TRUE),
    ('Laptop Dell Inspiron 14"', 3499.99, 12, 3, 3, TRUE),
    ('MacBook Air 13" M2', 5999.99, 8, 2, 3, TRUE),
    ('PC Gamer Asus ROG', 6499.99, 5, 2, 3, TRUE),
    ('Computadora de Escritorio Dell Optiplex', 2999.99, 10, 3, 3, TRUE),
    ('Mini PC Intel NUC', 2199.99, 7, 2, 3, TRUE),
    ('Laptop Lenovo ThinkPad X1', 4799.99, 6, 2, 3, TRUE),
    ('All-in-One HP 24"', 3299.99, 8, 2, 3, TRUE),
    ('Chromebook Acer 14"', 1799.99, 15, 5, 3, TRUE),
    ('Monitor Samsung 27" Curvo', 1299.99, 20, 5, 3, TRUE),
    
    -- Categoría 2: Electrodomésticos Cocina
    ('Refrigerador Samsung Side by Side 26 pies', 7999.99, 5, 2, 4, TRUE),
    ('Cocina a Gas Mabe 6 Hornillas', 1899.99, 8, 4, 4, TRUE),
    ('Microondas LG 1.5 pies', 699.99, 15, 3, 4, TRUE),
    ('Licuadora Oster 3 velocidades', 399.99, 25, 5, 4, TRUE),
    ('Batidora KitchenAid Stand Mixer', 1499.99, 10, 3, 4, TRUE),
    ('Cafetera Nespresso Essenza', 599.99, 18, 5, 4, TRUE),
    ('Tostadora Black & Decker 2 rebanadas', 149.99, 30, 8, 4, TRUE),
    ('Freidora de Aire Oster 4L', 499.99, 20, 5, 4, TRUE),
    ('Extractor de Jugos Philips', 349.99, 12, 4, 4, TRUE),
    ('Procesador de Alimentos Bosch', 799.99, 8, 3, 4, TRUE),
    
    -- Categoría 3: Electrodomésticos Lavandería
    ('Lavadora Samsung 18kg Carga Superior', 2999.99, 7, 2, 5, TRUE),
    ('Secadora Eléctrica Whirlpool 16kg', 2499.99, 6, 2, 5, TRUE),
    ('Lavaseca LG 12kg', 3799.99, 5, 2, 5, TRUE),
    ('Plancha a Vapor Black & Decker', 129.99, 25, 8, 5, TRUE),
    ('Aspiradora Robot Xiaomi', 899.99, 12, 3, 5, TRUE),
    ('Centro de Planchado Tefal', 599.99, 10, 3, 5, TRUE),
    ('Aspiradora Vertical Dyson V11', 1999.99, 8, 2, 5, TRUE),
    ('Plancha de Pelo Remington', 249.99, 15, 5, 5, TRUE),
    ('Secador de Pelo Philips', 199.99, 20, 5, 5, TRUE),
    ('Máquina de Coser Singer', 699.99, 8, 2, 5, TRUE),
    
    -- Categoría 4: Audio y Video
    ('Smart TV Samsung 65" 4K QLED', 5499.99, 10, 2, 6, TRUE),
    ('Smart TV LG 55" OLED', 4999.99, 8, 2, 6, TRUE),
    ('Barra de Sonido Samsung 5.1', 899.99, 12, 3, 6, TRUE),
    ('Home Theater Sony 7.1', 1799.99, 6, 2, 6, TRUE),
    ('Proyector Epson FullHD', 2299.99, 5, 2, 6, TRUE),
    ('Chromecast Google TV', 249.99, 25, 8, 6, TRUE),
    ('Roku Streaming Stick 4K', 279.99, 20, 5, 6, TRUE),
    ('Parlante Bluetooth JBL Charge 5', 599.99, 18, 5, 6, TRUE),
    ('Audífonos Sony WH-1000XM4', 1499.99, 15, 3, 6, TRUE),
    ('Reproductor Blu-ray Sony', 399.99, 10, 3, 6, TRUE),
    
    -- Categoría 5: Accesorios Tecnológicos
    ('Mouse Inalámbrico Logitech', 149.99, 30, 10, 7, TRUE),
    ('Teclado Mecánico Corsair', 399.99, 20, 5, 7, TRUE),
    ('Disco Duro Externo Seagate 2TB', 349.99, 25, 8, 7, TRUE),
    ('Memoria USB SanDisk 128GB', 79.99, 50, 15, 7, TRUE),
    ('Webcam Logitech HD', 249.99, 20, 5, 7, TRUE),
    ('Router WiFi TP-Link Mesh', 499.99, 15, 5, 7, TRUE),
    ('Powerbank Anker 20000mAh', 199.99, 30, 10, 7, TRUE),
    ('Cable HDMI 4K 2m', 59.99, 40, 15, 7, TRUE),
    ('Adaptador USB-C a HDMI', 89.99, 35, 10, 7, TRUE),
    ('Audífonos AirPods Pro', 999.99, 15, 3, 7, TRUE);
