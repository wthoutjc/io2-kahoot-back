from distutils.log import debug
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from mysql.connector.errors import Error
from werkzeug.security import generate_password_hash, check_password_hash

#JSON Web Tokens
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt

#Herramientas
import os                       # Creacion de randoms para config interna del server y manejo de enviroment
import json                     # Estructura json
import datetime                 # Manejo de fechas
from uuid import uuid4          # Asignación de códigos para update_password
from decimal import Decimal
import re

#Manejo de .xlsx
import pandas as pd                 # Manejo de DataFrames
from io import BytesIO

#Servicios AWS
import boto3

#SQL
from db.db import SQLOperations 

app = Flask(__name__)

#Operaciones SQL
sql_op = SQLOperations()

#Config del entorno
SECRET_KEY = '#$@Nx260D#'
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

jwt = JWTManager(app)

#Ruta raiz
@app.route("/")
def index():
    return 200

#Rutas SQL
@app.route("/login", methods=["POST"])
def log_in():
    print('log-in')
    #Borrar tokens vencidos de la lista block tokens en la DB
    # message, success = sql_op.clean_block_tokens()
    if request.data:
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)

        id_student = json_data['idStudent']

        if id_student:
            student, success = sql_op.consultar_usuario(id_student)
            if success:
                payload = {
                    'id': student[0],
                    'nombre': student[1],
                    'apellido': student[2],
                    'correo': student[3],
                    'proyecto': student[4],
                }
                access_token = create_access_token(identity=payload, expires_delta=datetime.timedelta(minutes=1)) #60
                return make_response(jsonify({"results": access_token}), 200)
            return make_response(jsonify({"results": student}), 500)
        return make_response(jsonify({"results": 'Usuario no ingresado'}), 500)
    return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

@app.route("/verifyJWT")
@jwt_required()
def verify_jwt():
    print('verify-jwt')
    return make_response(jsonify({"results": ['Token válido', True] }), 200)

if __name__ == '__main__':
    app.run(debug=True)