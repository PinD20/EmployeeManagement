USE db_project;

CREATE TABLE departamento (
    codigo INT PRIMARY KEY,
    nombre VARCHAR(35) NOT NULL
);

CREATE TABLE empleado (
    codigo              INT PRIMARY KEY,
    nombre              VARCHAR(50) NOT NULL,
    apellido            VARCHAR(50) NOT NULL,
    codigo_departamento INT NOT NULL,
    fecha_contratacion  DATE NOT NULL,
    cargo               VARCHAR(30) NOT NULL,
    FOREIGN KEY (codigo_departamento) REFERENCES departamento(codigo)
);