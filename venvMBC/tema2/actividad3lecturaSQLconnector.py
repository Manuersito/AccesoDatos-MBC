import mysql.connector
import time

try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2dam'
    )
    print("Conexión a la base de datos exitosa")
    cursor = conexion.cursor()
    start_time = time.time()
    # Consulta para obtener 10,000 registros
    cursor.execute("SELECT * FROM Moviles LIMIT 10000")
    resultados = cursor.fetchall()
    
    end_time = time.time()
    print(f"Tiempo de lectura con mysql.connector: {end_time - start_time} segundos")

finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada")
