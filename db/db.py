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