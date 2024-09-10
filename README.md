# Employee Management

Este proyecto se basa en una aplicación web para el manejo de empleados. Cada empleado cuenta con los siguientes campos:
- Código de empleado
- Nombre
- Apellido
- Departamento
- Cargo
- Fecha de contratación

La aplicación cuenta con tres capas: la capa de presentación (frontend), que se encuentra realizada con Angular; la capa de lógica de negocio (backend), que se encuentra realizada con Python y Flask-RestX; y la capa de datos que se encuentra implementada mediante una base de datos MySQL dockerizada.

## Ejecución de la aplicación

Para ejecutar la aplicación es necesario realizar una serie de pasos que se explican a continuación.

### Base de Datos
Para levantar el contenedor es indispensable tener instalado Docker.

Luego, con una terminal se debe posicionar en la carpeta de db y ejecutar el siguiente comando:
```
docker build -t db-name .
```
Con esto se creará la imagen de docker y para ejecutarla se utiliza el siguiente comando.
```
docker run -d -p 3306:3306 db-name
```

### Backend
Para ejecutar el backend primero se debe contar con Python instalado y luego se debe instalar las siguientes librerías.
```
pip install flask-restx
pip install mysql-connector-python
pip install python-dotenv
pip install flask-cors
```
Para ejecutar el backend se utiliza el siguiente comando.
```
python api.py
```

### Frontend
Para el frontend se requiere acceder a la carpeta de frontend desde una terminarl y ejecutar el siguiente comando para instalar las dependecias.
```
npm install
```

Luego de realizar esto, podemos ejecutar el frontend de la siguiente forma.
```
ng serve
```

