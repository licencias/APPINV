CREATE TABLE usuario (
    id_usuario int NOT NULL AUTO_INCREMENT,
    nombre varchar(100),
    rut varchar(15),
    PRIMARY KEY (id_usuario)
);

CREATE TABLE factura (
    id_factura int NOT NULL AUTO_INCREMENT,
    nombre_proveedor varchar(100),
    rut_proveedor varchar(20),
    PRIMARY KEY (id_factura)
);

CREATE TABLE detalle_factura (
    id_detalle_factura int NOT NULL AUTO_INCREMENT,
    id_factura int,
    identificador_producto varchar(255),
    nombre_producto varchar(255),
    fecha_factura varchar(255),
    cantidad varchar(255),
    PRIMARY KEY (id_detalle_factura),
    FOREIGN KEY (id_factura) REFERENCES factura(id_factura)
);

CREATE TABLE registro_componente (
    id_registro_componente int NOT NULL AUTO_INCREMENT,
    id_detalle_factura int,
    nombre_producto varchar(50), 
    quality_assurance int,    
    fecha_produccion varchar(100),
    id_usuario int,
    tipo_producto varchar(50),
    estado_disponibilidad varchar(10),
    PRIMARY KEY (id_registro_componente),
    FOREIGN KEY (id_detalle_factura) REFERENCES detalle_factura(id_detalle_factura),  
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)  
);

CREATE TABLE detalle_registro_componente (
    id_detalle_registro_componente int NOT NULL AUTO_INCREMENT,
    id_registro_componente int,
    PRIMARY KEY (id_detalle_registro_componente),
    FOREIGN KEY (id_registro_componente) REFERENCES registro_componente(id_registro_componente)
);

CREATE TABLE mert(
    id_mert int NOT NULL AUTO_INCREMENT,
    rut_usuario varchar(255),
    fecha_produccion varchar(255),
    serial_salida varchar(255),
    qa int,
    disponibilidad int,
    id_registro_componente int,
    PRIMARY KEY (id_mert),
    FOREIGN KEY (id_registro_componente) REFERENCES registro_componente(id_registro_componente)
);

CREATE TABLE mert_produccion (
    id_mert_produccion int NOT NULL AUTO_INCREMENT,
    descripcion varchar(255),
    nombre_cliente varchar(255),
    rut_cliente varchar(255),
    fecha_salida varchar(255),
    serial_salida varchar(255),
    flota_destino varchar(255),
    id_mert int,
    PRIMARY KEY (id_mert_produccion),
    FOREIGN KEY (id_mert) REFERENCES mert(id_mert)
);
