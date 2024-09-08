from flask import Flask
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
        if conn and conn.is_connected():
            with conn.cursor() as cursor:
                result = cursor.execute("SELECT * FROM empleado")
                rows = cursor.fetchall()
            conn.close()
            return { 'employees': rows}, 200
        else:
            print("Could not connect")
        return { 'message': 'No fue posible conectar con la base de datos' }, 500
    
    def post(self):
        return {}, 200

@api.route('/api/empleados/<int:id>')
class Empleados_id(Resource):
    def put(self):
        return {}, 200
    
    def delete(self):
        return {}, 200
    
@api.route('/api/departamentos')
class Departamentos(Resource):
    def get(self):
        return {}, 500
    
if __name__ == '__main__':
    app.run(debug=True)