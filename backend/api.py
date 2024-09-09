from flask import Flask, request
from flask_restx import Api, Resource

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
api = Api(app)

# Conexión a base de datos
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

@api.route('/test')
class TestRoute(Resource):
    def get(self):
        return {'message': 'everything ok'}, 200

@api.route('/api/empleados')
class Empleados(Resource):
    def get(self):
        conn.reconnect()
        if conn and conn.is_connected():
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM empleado")
                headers = [x[0] for x in cursor.description]
                rows = cursor.fetchall()
            conn.close()

            json_data = []
            for row in rows:
                item = dict(zip(headers, row))

                if 'fecha_contratacion' in item:
                    item['fecha_contratacion'] = item['fecha_contratacion'].strftime('%Y-%m-%d')

                json_data.append(item)
            return { 'employees': json_data }, 200
        else:
            print("Could not connect")
        return { 'message': 'No fue posible obtener los datos de los empleados' }, 500
    
    def post(self):
        conn.reconnect()
        data = request.get_json()
        name = data['name']
        lastname = data['lastname']
        department_code = data['department_code']
        hiring_date = data['hiring_date']
        job = data['job']

        success = False
        if name and lastname and department_code and hiring_date and job:
            if conn and conn.is_connected():
                with conn.cursor() as cursor:
                    sql = 'INSERT INTO empleado (nombre, apellido, codigo_departamento, fecha_contratacion, cargo) VALUES (%s, %s, %s, %s, %s)'
                    values = (name, lastname, department_code, hiring_date, job)
                    cursor.execute(sql, values)
                    conn.commit()
                    success = cursor.rowcount > 0
                conn.close()
                if success:
                    return { 'message': 'Empleado registrado con éxito' }, 200
                return { 'message': 'No fue posible ingresar el nuevo empleado' }, 500
            else:
                print("Could not connect")            
        conn.close()
        return { 'message': 'Todos los campos son obligatorios para registrar un empleado'}, 500

@api.route('/api/empleados/<int:id>')
class Empleados_id(Resource):
    def put(self, id):
        conn.reconnect()
        data = request.get_json()
        name = data['name']
        lastname = data['lastname']
        department_code = data['department_code']
        hiring_date = data['hiring_date']
        job = data['job']

        success = False
        if id:
            if conn and conn.is_connected():
                if name and lastname and department_code and hiring_date and job:
                    with conn.cursor() as cursor:
                        sql = '''UPDATE empleado SET nombre = %s, apellido = %s,
                                    codigo_departamento = %s, fecha_contratacion = %s,
                                    cargo = %s
                                    WHERE codigo = %s'''
                        cursor.execute(sql, (name, lastname, department_code, hiring_date, job, id))
                        conn.commit()
                        success = cursor.rowcount > 0
                    conn.close()
                    if success:
                        return { 'message': 'Empleado actualizado con éxito' }, 200
                    return { 'message': 'No fue posible actualizar el empleado' }, 500
                else:
                    return { 'message': 'Todos los campos son obligatorios para actualizar un empleado' }, 500
            else:
                print("Could not connect")            
        conn.close()
        return { 'message': 'Es necesario proporcionar el código para actualizar el empleado'}, 500
    
    def delete(self, id):
        conn.reconnect()
        success = False
        if id:
            if conn and conn.is_connected():
                with conn.cursor() as cursor:
                    sql = 'DELETE FROM empleado WHERE codigo = %s'
                    cursor.execute(sql, (id, ))
                    conn.commit()
                    success = cursor.rowcount > 0
                conn.close()
                if success:
                    return { 'message': 'Empleado eliminado con éxito' }, 200
                return { 'message': 'No fue posible eliminar el empleado' }, 500
            else:
                print("Could not connect")            
        conn.close()
        return { 'message': 'Es necesario proporcionar el código para eliminar el empleado'}, 500
    
@api.route('/api/departamentos')
class Departamentos(Resource):
    def get(self):
        conn.reconnect()
        if conn and conn.is_connected():
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
            print("Could not connect")
        return { 'message': 'No fue posible obtener los datos de los departamentos' }, 500
    
if __name__ == '__main__':
    app.run(debug=True)