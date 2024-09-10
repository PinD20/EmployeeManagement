from flask import Flask, request
from flask_restx import Api, Resource
from flask_cors import CORS

import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

# Variables de entorno
load_dotenv()
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DATABASE')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

app = Flask(__name__)
CORS(app)
api = Api(app)

#Conexión inicial a base de datos
conn = None
try:
    conn = mysql.connector.connect(
        host = db_host,
        database = db_name,
        user = db_user,
        password = db_password
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid database username/password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Invalid database")
    else:
        print(err)

# Reconexión a base de datos
def connectDb():
    global conn
    if conn is not None:
        conn.reconnect() # Reestablecer conexión con la db
        if conn.is_connected():
            return True
    else:
        try:
            conn = mysql.connector.connect(
                host = db_host,
                database = db_name,
                user = db_user,
                password = db_password
            )
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Invalid database username/password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Invalid database")
            else:
                print(err)
            return False

@api.route('/test')
class TestRoute(Resource):
    def get(self):
        return {'apiMessage': 'everything ok'}, 200

@api.route('/api/empleados')
class Empleados(Resource):
    def get(self):
        if connectDb():
            with conn.cursor() as cursor:
                cursor.execute('''SELECT  em.codigo, em.nombre, em.apellido, dpto.codigo AS codigo_departamento, dpto.nombre AS departamento, em.fecha_contratacion, em.cargo
                                    FROM empleado em
                                    INNER JOIN departamento dpto ON em.codigo_departamento = dpto.codigo''')
                headers = [x[0] for x in cursor.description] # Recuperación de encabezados de la data
                rows = cursor.fetchall()
            conn.close()

            json_data = []
            for row in rows: #Formación de JSON para respuesta
                item = dict(zip(headers, row))
                if 'fecha_contratacion' in item:
                    item['fecha_contratacion'] = item['fecha_contratacion'].strftime('%m-%d-%Y')
                json_data.append(item)

            return { 'employees': json_data }, 200
        else:
            return { 'apiMessage': 'No fue posible establecer comunicación con la base de datos'}, 500
    
    def post(self):
        data = request.get_json()

        keys = ['nombre', 'apellido', 'fecha_contratacion', 'cargo']
        missing_keys = [key for key in keys if key not in data or not data[key].strip()]

        # Validación de campos obligatorios
        if missing_keys or 'codigo_departamento' not in data:
            return { 'apiMessage': 'Todos los campos son obligatorios para registrar un empleado'}, 500
        
        name = data['nombre']
        lastname = data['apellido']
        department_code = data['codigo_departamento']
        hiring_date = data['fecha_contratacion']
        job = data['cargo']

        if connectDb():
            with conn.cursor() as cursor:
                sql = 'INSERT INTO empleado (nombre, apellido, codigo_departamento, fecha_contratacion, cargo) VALUES (%s, %s, %s, %s, %s)'
                values = (name, lastname, department_code, hiring_date, job)
                try: # Ejecución de query
                    cursor.execute(sql, values)
                    conn.commit()
                except:
                    conn.rollback()
                    return { 'apiMessage': 'No fue posible registrar el nuevo empleado' }, 500
                
            conn.close()
            if cursor.rowcount > 0: # Validación de empleado registrado
                return { 'apiMessage': 'Empleado registrado con éxito' }, 200
            return { 'apiMessage': 'No fue posible ingresar el nuevo empleado' }, 500
        else:
            return { 'apiMessage': 'No fue posible establecer comunicación con la base de datos'}, 500

@api.route('/api/empleados/<int:id>')
class Empleados_id(Resource):
    def put(self, id):
        data = request.get_json()
        keys = ['nombre', 'apellido', 'fecha_contratacion', 'cargo']
        missing_keys = [key for key in keys if key not in data or not data[key].strip()]

        # Validación de campos obligatorios
        if missing_keys or 'codigo_departamento' not in data:
            return { 'apiMessage': 'Todos los campos son obligatorios para registrar un empleado'}, 500
        
        name = data['nombre']
        lastname = data['apellido']
        department_code = data['codigo_departamento']
        hiring_date = data['fecha_contratacion']
        job = data['cargo']
        
        if connectDb():
            if id:
                with conn.cursor() as cursor:
                    sql = '''UPDATE empleado SET nombre = %s, apellido = %s,
                                codigo_departamento = %s, fecha_contratacion = %s,
                                cargo = %s
                                WHERE codigo = %s'''
                    try:
                        cursor.execute(sql, (name, lastname, department_code, hiring_date, job, id))
                        conn.commit()
                    except:
                        conn.rollback()
                        return { 'apiMessage': 'No fue posible actualizar el empleado' }, 500
                conn.close()
                if cursor.rowcount > 0: # Validación de empleado actualizado
                    return { 'apiMessage': 'Empleado actualizado con éxito' }, 200
                return { 'apiMessage': 'No fue posible actualizar el empleado' }, 500          
            conn.close()
            return { 'apiMessage': 'Es necesario proporcionar el código para actualizar el empleado'}, 500
        else:
            return { 'apiMessage': 'No fue posible establecer comunicación con la base de datos'}, 500
    
    def delete(self, id):
        if connectDb():
            if id:
                with conn.cursor() as cursor:
                    sql = 'DELETE FROM empleado WHERE codigo = %s'
                    try:
                        cursor.execute(sql, (id, ))
                        conn.commit()
                    except:
                        conn.rollback()
                        return { 'apiMessage': 'No fue posible actualizar el empleado' }, 500
                conn.close()
                if cursor.rowcount > 0: # Validación de empleado eliminado
                    return { 'apiMessage': 'Empleado eliminado con éxito' }, 200
                return { 'apiMessage': 'No fue posible eliminar el empleado' }, 500
            conn.close()
            return { 'apiMessage': 'Es necesario proporcionar el código para eliminar el empleado'}, 500   
        else:
            return { 'apiMessage': 'No fue posible establecer comunicación con la base de datos'}, 500
        
    
@api.route('/api/departamentos')
class Departamentos(Resource):
    def get(self):
        if connectDb():
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM departamento")
                headers = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
            conn.close()
            json_data = []
            for row in rows:
                item = dict(zip(headers, row))
                json_data.append(item)
            return { 'departments': json_data }, 200
        else:
            return { 'apiMessage': 'No fue posible establecer comunicación con la base de datos'}, 500
    
if __name__ == '__main__':
    app.run(debug=True)