from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

#JSON Web Tokens
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt

#Herramientas
import json                     # Estructura json
import datetime                 # Manejo de fechas

#SQL
from db.db import SQLOperations 

#Calificaciones
from puntaje.puntaje import Puntaje

app = Flask(__name__)

#Operaciones SQL
sql_op = SQLOperations()

#Config del entorno
SECRET_KEY = '#$@Nx260D#'
CORS(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

jwt = JWTManager(app)

# Tiempo TOKEN
TOKEN_EXP = 45

# Sistema de calificaciones
puntaje = Puntaje(TOKEN_EXP)

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
            calificacion, success_ = sql_op.consultar_calificacion(id_student)
            if not success_:
                student, success = sql_op.consultar_usuario(id_student)
                if success:
                    payload = {
                        'id': student[0],
                        'nombre': student[1],
                        'apellido': student[2],
                        'correo': student[3],
                        'proyecto': student[4],
                    }
                    access_token = create_access_token(identity=payload, expires_delta=datetime.timedelta(minutes=TOKEN_EXP)) #60
                    return make_response(jsonify({"results": access_token}), 200)
                return make_response(jsonify({"results": student}), 500)
            return make_response(jsonify({"results": f'{id_student} ya realizó la prueba. Nota: {calificacion[1]}'}), 500)
        return make_response(jsonify({"results": 'Usuario no ingresado'}), 500)
    return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

@app.route("/verifyJWT")
@jwt_required()
def verify_jwt():
    print('verify-jwt')
    return make_response(jsonify({"results": ['Token válido', True] }), 200)

@app.route("/registrar", methods=['POST'])
def registrar():
    print('registrar')
    if request.method == 'POST':
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)
        message, success = sql_op.registrar_usuario(json_data['newStudent'])
        if success:
            return make_response(jsonify({"results": message}), 200)
        return make_response(jsonify({"results": message}), 500)
    return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

@app.route("/actualizar", methods=['POST'])
@jwt_required()
def actualizar():
    print('actualizar')
    if request.method == 'POST':
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)
        id = json_data['id']
        data = json_data['updateUser']
        message, success = sql_op.actualizar_usuario(id, data)
        if success:
            return make_response(jsonify({"results": message}), 200)
        return make_response(jsonify({"results": message}), 500)
    return make_response(jsonify({"results": 'Falló el procesamiento de la solicitud.'}), 500)

@app.route("/answers", methods=["POST"])
@jwt_required()
def answers():
    print('answers')
    data_raw = request.data.decode("utf-8")
    json_data = json.loads(data_raw)

    id_student = json_data['idStudent']
    try:
        answers  = json_data['answers']
    except:
        answers = None

    puntaje.set_id(id_student)
    puntaje.set_answers(answers)

    print(answers)

    calificacion = puntaje.calificar()

    message, success = sql_op.insertar_calificacion(id_student, calificacion)
    if success:
        message_, success_ = sql_op.insertar_respuestas(id_student,answers)
        if success_:
            return make_response(jsonify({"results": message_}), 200)        
        return make_response(jsonify({"results": message_}), 500)        
    return make_response(jsonify({"results": message}), 500)

@app.route("/calificacion/<id>")
@jwt_required()
def calificacion(id):
    print('calificacion')
    calificacion , success = sql_op.consultar_calificacion(id)
    if success:
        return make_response(jsonify({"results": calificacion}), 200)
    return make_response(jsonify({"results": calificacion}), 500)

@app.route("/ranking")
def ranking():
    print('ranking')
    ranking , success = sql_op.get_ranking()
    if success:
        return make_response(jsonify({"results": ranking}), 200)
    return make_response(jsonify({"results": ranking}), 500)

if __name__ == '__main__':
    app.run(debug=True)