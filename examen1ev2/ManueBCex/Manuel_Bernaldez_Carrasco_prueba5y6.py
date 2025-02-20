from pymongo import MongoClient


class DatabaseManager:
    def __init__(self, db_name="1dam", collection_name="productos"):
        """Inicializa el componente DatabaseManager."""
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None
    


    def insertar_productos(self, productos):
        
        self.insert_many(productos)
        
    #def consultar_proyeccion_ordenada(self, filtro, proyeccion, orden):
        
    def mostrar_todos_productos(self):
        print("Documentos en la colección:")
        self.documentos = coleccion.find()
        for documento in self.documentos:
            print(documento)
            
            
    def actualizar_productos(self, filtro, actualizacion):
        self.mostrar_todos_productos()
        
        self.coleccion_herramientas.update_many(
            filtro,
            actualizacion
        )
        
        self.mostrar_todos_productos()
        
        
    def contar_documentos(self):
        self.total =  productos.count_documents({})
        print(total)
        
        
    def eliminar_documentos(self, filtro):
        self.contar_documentos()
        self.productos.delete_many({"stock:" < filtro})
        self.contar_documentos()
        
        
    #def consulta_compleja(self, filtro, proyeccion, orden):

    def cerrar_conexion(self):
        if self.client:
                self.client.close()
        
        
if __name__ == "__main__":
    # Configurar el componente
    db_manager = DatabaseManagerDocumental(

        database_name="1dam",
        collection_name="productos"
    )
    db_manager.conectar()
    try:
        producto = [
        {"nombre": "Drone Phantom X", "categoria": "Drones", "precio": 1200.50, "stock": 8},
        {"nombre": "Auriculares Sonic Boom", "categoria": "Auriculares", "precio": 299.99, "stock": 15},
        {"nombre": "Cámara Action Pro", "categoria": "Cámaras", "precio": 499.99, "stock": 10},
        {"nombre": "Asistente SmartBuddy", "categoria": "Asistentes Inteligentes", "precio": 199.99,
        "stock": 20},
        {"nombre": "Cargador Solar Ultra", "categoria": "Accesorios", "precio": 49.99, "stock": 3}
    ]
        
        #tarea 1
        db_manager.insertar_productos(producto)

        filtroact = {"nombre": "Drone Phantom X", "nombre":"Cámara Action Pro"}
        actualizacion = {"precio": "1300"}
        #tarea 3
        db_manager.actualizar_productos(filtroact,actualizacion)

        #tarea 4
        db_manager.eliminar_documentos(5)

        db_manager.cerrar_conexion()
    except Exception as e:
        logging.error(f"Error general: {e}")
        db_manager.revertir_transaccion()
    finally:
        db_manager.desconectar()
