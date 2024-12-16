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
    
    # Intentar acceder a la base de datos para verificar la conexión
    colecciones = db.list_collection_names()
    
    print("Conexión exitosa. Colecciones en la base de datos:")
    print(colecciones)
    
    # Acceder a la colección Moviles
    coleccion = db['Moviles']
    
    # 1. Consultar con sistema "android"
    resultado = coleccion.find({ 'Sistema': 'android' })
    print("\nMóviles con sistema Android:")
    for movil in resultado:
        print(movil)
    
    # 2. Proyección: Mostrar solo Marca y Modelo, excluyendo _id
    resultado = coleccion.find(
        { 'Sistema': 'android' }, 
        { '_id': 0, 'Marca': 1, 'Modelo': 1 }
    )
    print("\nMóviles con sistema Android (solo Marca y Modelo):")
    for movil in resultado:
        print(movil)
    
    # 3. Limitar a 2 resultados y ordenar por Marca (alfabéticamente)
    resultado = coleccion.find(
        { 'Sistema': 'android' }, 
        { '_id': 0, 'Marca': 1, 'Modelo': 1 }
    ).sort('Marca', 1).limit(2)
    
    print("\nPrimeros 2 móviles con sistema Android, ordenados por Marca:")
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
