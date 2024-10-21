import mysql.connector
from mysql.connector import Error
import time, random

try:
    conexion = mysql.connector.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='2dam'
    )
    if conexion.is_connected():
        print("Conexión a la base de datos exitosa")
        cursor = conexion.cursor()
        start_time = time.time()
        
        Marca = ["Xiaomi", "Iphone", "Samsung", "Google"]
        Modelo = ["model1", "model2", "model3", "model4"]
        Sistema_operativo = ["android 14", "android 12", "android 13"]
        Capacidad = ["128 GB", "256 GB", "1 TB"]
        precio = ["200€", "500€", "800€", "1000€"]
        
        for i in range(0, 10001):
            marca = random.choice(Marca)
            modelo = random.choice(Modelo)
            sistema_operativo = random.choice(Sistema_operativo)
            capacidad = random.choice(Capacidad)
            Precio = random.choice(precio)
            cursor.execute(
                "INSERT INTO Moviles (Marca, Modelo, Sistema_Operativo, Capacidad, Precio) VALUES (%s, %s, %s, %s, %s)",
                (marca, modelo, sistema_operativo, capacidad, Precio)
            )
        conexion.commit()
        end_time = time.time()
        print(f"Tiempo de inserción con mysql-connector: {end_time - start_time} segundos")
        
finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("Conexión cerrada")
