from pymongo import MongoClient, errors

# Datos de conexión
usuario = "usuario"
clave = "usuario"
base_datos = "1dam"
host = "localhost"
puerto = 27017

try:
    # Intentar conectarse al servidor MongoDB
    client = MongoClient(f"mongodb://{usuario}:{clave}@{host}:{puerto}/{base_datos}",
                         serverSelectionTimeoutMS=5000)
    
    # Seleccionar la base de datos
    db = client[base_datos]
    
    # Acceder a la colección Moviles
    coleccion = db['Moviles']
    
    # 1. Añadir tres documentos a la colección
    documentos = [
        {"Marca": "Xiaomi", "Modelo": "mi 14", "Capacidad": "128GB", "Sistema": "android"},
        {"Marca": "Samsung", "Modelo": "galaxy s24", "Capacidad": "512GB", "Sistema": "android"},
        {"Marca": "Iphone", "Modelo": "17 pro", "Capacidad": "256GB", "Sistema": "ios"}
    ]
    coleccion.insert_many(documentos)
    print("Se han añadido tres documentos a la colección.")
    
    # Mostrar el estado antes de la actualización
    print("\nEstado antes de la actualización:")
    resultado = coleccion.find({ 'Sistema': 'android' })
    for movil in resultado:
        print(movil)
    
    # 2. Actualizar un campo de un sólo documento
    coleccion.update_one(
        {"Modelo": "mi 14"},  # Condición para encontrar el documento
        {"$set": {"Capacidad": "256GB"}}  # Actualización del campo "Capacidad"
    )
    print("\nSe ha actualizado el campo 'Capacidad' del modelo 'mi 14' a '256GB'.")
    
    # Mostrar el estado después de la actualización
    print("\nEstado después de la actualización:")
    resultado = coleccion.find({ 'Sistema': 'android' })
    for movil in resultado:
        print(movil)
    
    # 3. Eliminar uno de los documentos
    coleccion.delete_one({"Modelo": "galaxy s24"})  # Eliminar el documento con el modelo 'galaxy s24'
    print("\nSe ha eliminado el documento con el modelo 'galaxy s24'.")
    
    # Mostrar el estado después de la eliminación
    print("\nEstado después de la eliminación:")
    resultado = coleccion.find({ 'Sistema': 'android' })
    for movil in resultado:
        print(movil)

except errors.ServerSelectionTimeoutError as err:
    # Este error ocurre si el servidor no está disponible o no se puede conectar
    print(f"No se pudo conectar a MongoDB: {err}")
except errors.OperationFailure as err:
    # Este error ocurre si las credenciales son incorrectas o no se tienen los permisos necesarios
    print(f"Fallo en la autenticación o permisos insuficientes: {err}")
except Exception as err:
    # Manejar cualquier otro error inesperado
    print(f"Ocurrió un error inesperado: {err}")
finally:
    # Cerrar la conexión si se estableció correctamente
    if 'client' in locals():
        client.close()
        print("Conexión cerrada.")
