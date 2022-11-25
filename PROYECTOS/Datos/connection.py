import mysql.connector
from mysql.connector import Error


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    db="db_farmacia"
    
)

try:
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute("select database();")
        db = cursor.fetchone()

        print("Se ha conectado a la BD: ", db)
except Error as e:
    print("Error al conectar a MySQL: ", e)
#finally:
#    if connection.is_connected():
#        cursor.close()
#        connection.close()
#        print("La conexion a MySQL se ha cerrado!")