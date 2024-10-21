import pymysql
from pymysql.err import MySQLError

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2dam'
    )
    print("Conexión a la base de datos exitosa")

    cursor = conexion.cursor()

    cursor.execute("SELECT id, Marca, Modelo, Sistema_Operativo, Capacidad, Precio, Tienda_id FROM Moviles LIMIT 5")
    
    print("\nMostrando resultados uno por uno:")
    
    fila = cursor.fetchone()
    while fila:
        print(f"ID: {fila[0]}, marca: {fila[1]}, modelo: {fila[2]}, sistemaOperativo: {fila[3]}, capacidad: {fila[4]}, precio: {fila[5]}, ID Tienda: {fila[6]}")
        fila = cursor.fetchone()

    cursor.close()

    cursor = conexion.cursor()

    cursor.execute("SELECT id, Marca, Modelo, Sistema_Operativo, Capacidad, Precio, Tienda_id FROM Moviles LIMIT 5")
    
    print("\nMostrando resultados uno por uno:")
    
    fila = cursor.fetchone()
    while fila:
        print(f"ID: {fila[0]}, marca: {fila[1]}, modelo: {fila[2]}, sistemaOperativo: {fila[3]}, capacidad: {fila[4]}, precio: {fila[5]}, ID Tienda: {fila[6]}")
        fila = cursor.fetchone()

    cursor.close()

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    # Cerrar la conexión a la base de datos si está abierta
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
