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

    cursor.execute("DELETE FROM Moviles WHERE Tienda_id = %s", (1))
    conexion.commit()
    print(cursor.rowcount, "registro(s) eliminado(s)")

except MySQLError as e:
    print(f"Error de conexión a MySQL: {e}")
    
finally:
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
