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
    cursor.execute("""
        CREATE TABLE if not exists Moviles (
         id int AUTO_INCREMENT PRIMARY KEY,
         Marca varchar(50),
         Modelo varchar(50),
         Sistema_Operativo varchar(50),
         Capacidad varchar(50),
         Precio varchar(50)
        )
    """)
    cursor.execute(
        "INSERT INTO Moviles (Marca, Modelo, Sistema_Operativo, Capacidad, Precio) VALUES (%s, %s, %s, %s, %s)",
        ("Xiaomi", "Mi 13", "Hyper OS", "256 GB", "180€")
    )
    conexion.commit()
    cursor.execute("SELECT * FROM Moviles")
    for fila in cursor.fetchall():
        print(fila)
except MySQLError as e:
    print(f"Error en la operación MySQL: {e}")
finally:

    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
