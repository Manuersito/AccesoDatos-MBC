import pymysql
from pymysql.err import MySQLError

try:
    # Conectar a la base de datos
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2dam'
    )
    print("Conexión a la base de datos exitosa")

    marca_input = input("Introduce la marca (por ejemplo, 'Xiaomi','Smsung','Google' o ''Iphone): ")

    cursor = conexion.cursor()

    cursor.callproc('contar_moviles', (marca_input,))

    resultados = cursor.fetchall()
    for resultado in resultados:
        print(f"Número de moviles para la marca '{marca_input}': {resultado[0]}")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    # Cerrar el cursor y la conexión a la base de datos si están abiertos
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
