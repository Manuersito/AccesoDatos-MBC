import pymysql

try:
    conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2dam'
        
    )    
    if conexion:
        print("Conexion exitosa")
except pymysql.MySQLError as e:
    print(e)
    
finally:
    if conexion:
        conexion.close
        print("Conexion cerrada")