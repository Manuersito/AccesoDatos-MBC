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
        CREATE TABLE if not exists Tiendas (
         id int AUTO_INCREMENT PRIMARY KEY,
         Nombre varchar(50),
         Direccion varchar(50)
        )
    """)
    
    print("Tabla creada")
    cursor.execute("""
        ALTER TABLE Moviles ADD Tienda_id INT,
        ADD CONSTRAINT fk_proveedor
        FOREIGN KEY (Tienda_id) REFERENCES Tiendas(id)
    """)
    print("Foreing key creada")
    conexion.commit()
    
except MySQLError as e:
    print(f"Error en la operación MySQL: {e}")
finally:

    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
