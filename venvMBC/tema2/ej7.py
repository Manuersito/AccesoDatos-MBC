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

    print("Iniciando transacción...")
    # Insertar un nuevo registro en la tabla Moviles

    sql_insert = """
        INSERT INTO Moviles (Marca, Modelo, Sistema_Operativo, Capacidad, Precio, Tienda_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    datos_moviles = ("Samsung", "galaxy", "android 14", "256 GB", "1000", "4")
    #Le introducimos el dato id_tienda = "4", forzando el fallo ya que el solo tenemos hasta el id = "3" en la tabla tiendas
    cursor.execute(sql_insert, datos_moviles)
    # Hacer commit si todo va bien
    conexion.commit()
    print("Transacción exitosa: Registro insertado correctamente.")

except MySQLError as e:
    # Si ocurre un error, hacer rollback
    print(f"Error en la transacción: {e}")
    if conexion:
        conexion.rollback()
        print("Se realizó rollback.")
    
finally:
    # Cerrar la conexión a la base de datos si está abierta
    if 'conexion' in locals() and conexion.open:
        cursor.close()
        conexion.close()
        print("Conexión cerrada")