import pymysql,time,random
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
    start_time = time.time()
    
    Marca = ["Xiaomi","Iphone","Samsung","Google"]
    Modelo = ["model1","model2","model3","model4"]
    Sistema_operativo = ["android 14", "android 12", "android 13"]
    Capacidad = ["128 GB", "256 GB", "1 TB"]
    precio = ["200€","500€","800€","1000€"]
    
    for i in range(0,10001):
        marca = random.choice(Marca)
        modelo = random.choice(Modelo) 
        sistema_operativo= random.choice(Sistema_operativo)
        capacidad = random.choice(Capacidad)
        Precio= random.choice(precio)
        cursor.execute(
            "INSERT INTO Moviles (Marca, Modelo, Sistema_Operativo, Capacidad, Precio) VALUES (%s, %s, %s, %s, %s)",
            (marca,modelo,sistema_operativo,capacidad,Precio)
        )
    
    
    end_time = time.time()
    print(f"Tiempo de inserción con PyMySQL: {end_time - start_time} segundos")
    
finally:
    conexion.commit()
    if 'conexion' in locals() and conexion.open:
        conexion.close()
        print("Conexión cerrada")
