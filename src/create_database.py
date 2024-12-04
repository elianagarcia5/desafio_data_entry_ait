import mysql.connector
from mysql.connector import Error

def ejecutar_script_sql(host, user, password, database, script_path):
    conexion = None
    cursor = None
    try:
        # Conectar con la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            
            # Leer el script SQL con la codificación (UTF-8)
            with open(script_path, 'r', encoding='utf-8') as file:
                sql_script = file.read()

            # Cursor para ejecutar el script
            cursor = conexion.cursor()

            # Ejecutar el script SQL
            for resultado in cursor.execute(sql_script, multi=True):
                print(f"Ejecutando script: {resultado}")

            # Confirmar
            conexion.commit()
            print("Script ejecutado con éxito")

    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    except UnicodeDecodeError as e:
        print(f"Error de decodificación del archivo SQL: {e}")
    finally:
        if conexion is not None and conexion.is_connected():
            if cursor is not None:
                cursor.close()
            conexion.close()
            print("Conexión cerrada")

# Configuración de la conexión y ruta del script SQL
host = 'localhost'
user = 'root'
password = '123456'
database = 'aitsolutions'
script_path = r'C:\Users\nCuello\Desktop\AIT solutions\desafio_data_entry_ait\sql_scripts\desafio_data_entry_ait.sql'


ejecutar_script_sql(host, user, password, database, script_path)
