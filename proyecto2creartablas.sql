CREATE TABLE usuario (
    IDUsuario INT PRIMARY KEY,
    username varchar(12) NOT NULL,
    UserPassword varchar(12) NOT NULL,
    email varchar(40) NOT NULL,
    activo BOOLEAN NOT NULL,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    fechaNacimiento DATE,
    direccion varchar(60),
    altura INT,
    clasificacion BOOLEAN NOT NULL, 
    suscripcion INT,
    fechaInicio DATE NOT NULL,
    fechaFin DATE
);

CREATE TABLE smartwatch (
    IDSmartwatch INT PRIMARY KEY,
    IDUsuario INT, 
    CONSTRAINT fk_usuario
        FOREIGN KEY(IDUsuario)
            REFERENCES usuario(IDUsuario)
);

CREATE TABLE instructor (
    IDInstructor INT PRIMARY KEY,
    nombre varchar(30),
    apellido varchar(30),
    activo BOOLEAN NOT NULL,
    fechaInicio DATE NOT NULL,
    fechaFinal DATE
);
CREATE TABLE categoria (
    IDCategoria INT PRIMARY KEY,
    nombre varchar(20)
);



CREATE TABLE sesion (
    IDSesion INT PRIMARY KEY,
    IDInstructor INT NOT NULL,
    IDCategoria INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    duracion INT NOT NULL,
    CONSTRAINT fk_instructor
        FOREIGN KEY(IDInstructor)
            REFERENCES instructor(IDInstructor),
    CONSTRAINT fk_categoria
        FOREIGN KEY(IDCategoria)
            REFERENCES categoria(IDCategoria),
    UNIQUE (IDInstructor, fecha, hora)
);

CREATE TABLE UsuarioSesion (
    IDUsuario INT,
    IDSesion INT,
    CONSTRAINT fk_usuario
        FOREIGN KEY(IDUsuario)
            REFERENCES usuario(IDUsuario),
    CONSTRAINT fk_sesion
        FOREIGN KEY(IDSesion)
            REFERENCES sesion(IDSesion) ON DELETE CASCADE,
    UNIQUE (IDUsuario, IDSesion)
);


CREATE TABLE infoPago (
    IDUsuario INT,
    numTajeta VARCHAR(16),
    nombreTarjeta varchar(60),
    CONSTRAINT fk_usuario
        FOREIGN KEY(IDUsuario)
            REFERENCES usuario(IDUsuario)
);

CREATE TABLE nutricionista (
    IDNutricionista INT PRIMARY KEY,
    nombre varchar(30),
    apellido varchar(30),
    activo BOOLEAN NOT NULL,
    fechaInicio DATE NOT NULL,
    fechaFin DATE
);

CREATE TABLE consulta (
    IDConsulta INT PRIMARY KEY,
    IDUsuario INT,
    IDNutricionista INT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY(IDUsuario)
            REFERENCES usuario(IDUsuario),
    CONSTRAINT fk_nutricionista
        FOREIGN KEY(IDNutricionista)
            REFERENCES nutricionista(IDNutricionista)
); 

CREATE TABLE registro (
    IDUsuario INT,
    calorias INT,
    pesoActual float(4),
    fecha DATE NOT NULL,
    CONSTRAINT fk_usuario
        FOREIGN KEY (IDUsuario)
            REFERENCES usuario(IDUsuario),
    UNIQUE (IDUsuario, fecha)
);




