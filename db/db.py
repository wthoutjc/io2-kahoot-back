import mysql.connector
from mysql.connector import errors

#Settings
from db.settings import SETTINGS

#Manejo de fechas
import datetime

class SQLOperations():
    def __init__(self):
        '''
        Configuración de la base de datos MySQL
        '''
        self.host = SETTINGS["host"]
        self.user = SETTINGS["user"]
        self.passwd = SETTINGS["passwd"]
        self.database = SETTINGS["database"]
        self.based = None
        self.ncursor = None

    #Config Access
    def login_database(self):
        '''
        Iniciamos una conexion a la base de datos.
        '''
        try:
            self.based = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.passwd,
                    database=self.database
                )
            return self.based.cursor()
        except mysql.connector.Error as error:
            print('Login database Error: ' + str(error))
            return False

    def logout_database(self, ncursor):
        '''
        Cerramos la conexión a la base de datos.
        Args:
            ncursor: mysql.connector
        '''
        try:
            self.ncursor = ncursor
            self.ncursor.close()
            self.based.close()
            self.based = None
        except mysql.connector.Error as error:
            print('Logout database Error: ' + str(error))
            return False
    
    def consultar_usuario(self, id):
        '''
        Consulta la información específica de un estudiante
        Args:
            id: int
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM students WHERE k_students = %s"
            self.ncursor.execute(self.query, (id, ))
            result = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if result:
                return [result,True]
            return ['Estudiante no encontrado', False]
        except mysql.connector.Error as error:
            print('Consultar estudiante Error: ' + str(error))
            return ['Consultar estudiante Error: ', False]
    
    def registrar_usuario(self, data):
        '''
        Registrar un nuevo estudiante en el sistema
        Args: Dicc
            data = {
                id,
                nombre,
                apellido,
                correo,
                proyecto
            }
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "INSERT INTO students VALUES (%s, %s, %s, %s, %s)"
            self.ncursor.execute(self.query, (data['id'], data['nombre'], data['apellido'], data['correo'], data['proyecto']))
            self.based.commit()
            self.logout_database(self.ncursor)
            return ['Estudiante registrado satisfactoriamente', True]
        except mysql.connector.Error as error:
            print('Registrar estudiante Error: ' + str(error))
            return ['Registrar estudiante Error: ', False]
    
    def actualizar_usuario(self, id, data):
        '''
        Actualizar la información de un estudiante
        Args: Dicc
        '''
        try:
            self.ncursor = self.login_database()
            self.ncursor.execute("SET SQL_SAFE_UPDATES = 0")
            self.query = "UPDATE students SET k_students = %s, n_nombre = %s, n_apellido = %s, n_correo = %s, n_proyecto = %s WHERE k_students = %s"
            self.ncursor.execute(self.query, (data['id'], data['nombre'], data['apellido'], data['correo'], data['proyecto'], id))
            self.based.commit()
            self.logout_database(self.ncursor)
            return ['Información actualizada correctamente', True]
        except mysql.connector.Error as error:
            print('Actualizar estudiante Error: ' + str(error))
            return ['Actualizar estudiante Error: ', False]
    
    def insertar_calificacion(self, id, calificacion):
        print(calificacion)
        '''
        Inserta la calificiación de un estudiante en la base de datos
        SOLO SE PUEDE HACER 1 VEZ
        Args
            -id . INT codigo estudainte
            -calificacion INT nota
        '''
        try:
            # VERIFICAMOS QUE NO HAYA SIDO CALIFICADO ANTES
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM calificacion WHERE k_students = %s"
            self.ncursor.execute(self.query, (id,))
            calificacion_ = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if not calificacion_:
                # Insertamos calificación
                self.ncursor = self.login_database()
                self.query = "INSERT INTO calificacion VALUES (%s, %s)"
                self.ncursor.execute(self.query, (id, calificacion))
                self.based.commit()
                self.logout_database(self.ncursor)
                return ['Calificación añadida satisfactoriamente', True]
            return ['El estudiante ya ha sido calificado', False]
        except mysql.connector.Error as error:
            print('Insertar calificación Error: ' + str(error))
            return ['Insertar calificación Error: ', False]

    def insertar_respuestas(self, id_student, answers):
        '''
        Inserta las respuestas de cada estudiante
        '''
        try:
            aux = 1
            self.ncursor = self.login_database()
            self.query = "INSERT INTO preguntas VALUES (%s,%s,%s,%s)"
            if answers:
                for answer in answers.values():
                    if answer[0]:
                        self.ncursor.execute(self.query, (id_student,aux,answer[0],answer[1]))
                        self.based.commit()
                        aux += 1
                    else:
                        self.ncursor.execute(self.query, (id_student,aux,0,0))
                        self.based.commit()
                        aux += 1
            self.logout_database(self.ncursor)
            return ['Calificación añadida satisfactoriamente', True]
        except mysql.connector.Error as error:
            print('Insertar respuesta Error: ' + str(error))
            return ['Insertar respuesta Error: ', False]

    def consultar_calificacion(self, id):
        '''
        Consulta la calficacion de un estudiante
        Args
            id INT codigo
        '''
        try:
            # VERIFICAMOS QUE NO HAYA SIDO CALIFICADO ANTES
            self.ncursor = self.login_database()
            self.query = "SELECT * FROM calificacion WHERE k_students = %s"
            self.ncursor.execute(self.query, (id,))
            calificacion = self.ncursor.fetchone()
            self.logout_database(self.ncursor)
            if calificacion:
                return [calificacion, True]
            return ['El estudiante no ha sido calificado', False]
        except mysql.connector.Error as error:
            print('Consultar calificación Error: ' + str(error))
            return ['Consultar calificación Error: ', False]
    
    def get_ranking(self):
        '''
        Devuelve el ranking de puntajes
        '''
        try:
            self.ncursor = self.login_database()
            self.query = "SELECT CONCAT(students.n_nombre,' ',students.n_apellido) AS nombre, calificacion.q_calificacion FROM students, calificacion WHERE students.k_students = calificacion.k_students ORDER BY q_calificacion DESC;"
            self.ncursor.execute(self.query)
            ranking = self.ncursor.fetchall()
            self.logout_database(self.ncursor)
            if ranking:
                return [ranking, True]
            return ['No se han registrado respuestas aún.', False]
        except mysql.connector.Error as error:
            print('Consultar ranking Error: ' + str(error))
            return ['Consultar ranking Error: ', False]