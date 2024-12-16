import logging
import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_mobile.log"),  # Logs guardados en un archivo
        logging.StreamHandler(),  # Logs también en consola
    ]
)

class Movil(Persistent):
    """Clase que representa un móvil."""
    def __init__(self, modelo, marca, sistema_operativo, ram, almacenamiento):
        self.modelo = modelo
        self.marca = marca
        self.sistema_operativo = sistema_operativo
        self.ram = ram
        self.almacenamiento = almacenamiento

class DatabaseManagerObject:
    """Componente para gestionar bases de datos orientadas a objetos con ZODB."""
    def __init__(self, filepath="moviles.fs"):
        self.filepath = filepath
        self.db = None
        self.connection = None
        self.root = None
        self.transaccion_iniciada = False

    def conectar(self):
        """Conecta a la base de datos ZODB."""
        try:
            storage = FileStorage.FileStorage(self.filepath)
            self.db = DB(storage)
            self.connection = self.db.open()
            self.root = self.connection.root()
            if "moviles" not in self.root:
                self.root["moviles"] = {}
                transaction.commit()
            logging.info("Conexión establecida con ZODB.")
        except Exception as e:
            logging.error(f"Error al conectar a ZODB: {e}")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        try:
            if self.connection:
                self.connection.close()
            if self.db:
                self.db.close()
            logging.info("Conexión a ZODB cerrada.")
        except Exception as e:
            logging.error(f"Error al cerrar la conexión a ZODB: {e}")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        try:
            transaction.begin()
            self.transaccion_iniciada = True
            logging.info("Transacción iniciada.")
        except Exception as e:
            logging.error(f"Error al iniciar la transacción: {e}")

    def confirmar_transaccion(self):
        """Confirma la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.commit()
                self.transaccion_iniciada = False
                logging.info("Transacción confirmada.")
            except Exception as e:
                logging.error(f"Error al confirmar la transacción: {e}")

    def revertir_transaccion(self):
        """Revierte la transacción."""
        if self.transaccion_iniciada:
            try:
                transaction.abort()
                self.transaccion_iniciada = False
                logging.info("Transacción revertida.")
            except Exception as e:
                logging.error(f"Error al revertir la transacción: {e}")

    def crear_movil(self, id, modelo, marca, sistema_operativo, ram, almacenamiento):
        """Crea y almacena un nuevo móvil."""
        try:
            if id in self.root["moviles"]:
                raise ValueError(f"Ya existe un móvil con ID {id}.")
            self.root["moviles"][id] = Movil(modelo, marca, sistema_operativo, ram, almacenamiento)
            logging.info(f"Móvil con ID {id} creado exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear el móvil con ID {id}: {e}")

    def leer_moviles(self):
        """Lee y muestra todos los móviles almacenados."""
        try:
            moviles = self.root["moviles"]
            for id, movil in moviles.items():
                logging.info(
                    f"ID: {id}, Modelo: {movil.modelo}, Marca: {movil.marca}, "
                    f"Sistema Operativo: {movil.sistema_operativo}, RAM: {movil.ram}GB, "
                    f"Almacenamiento: {movil.almacenamiento}GB"
                )
            return moviles
        except Exception as e:
            logging.error(f"Error al leer los móviles: {e}")

    def actualizar_movil(self, id, modelo, marca, sistema_operativo, ram, almacenamiento):
        """Actualiza los atributos de un móvil."""
        try:
            movil = self.root["moviles"].get(id)
            if not movil:
                raise ValueError(f"No existe un móvil con ID {id}.")
            movil.modelo = modelo
            movil.marca = marca
            movil.sistema_operativo = sistema_operativo
            movil.ram = ram
            movil.almacenamiento = almacenamiento
            logging.info(f"Móvil con ID {id} actualizado exitosamente.")
        except Exception as e:
            logging.error(f"Error al actualizar el móvil con ID {id}: {e}")

    def eliminar_movil(self, id):
        """Elimina un móvil por su ID."""
        try:
            if id not in self.root["moviles"]:
                raise ValueError(f"No existe un móvil con ID {id}.")
            del self.root["moviles"][id]
            logging.info(f"Móvil con ID {id} eliminado exitosamente.")
        except Exception as e:
            logging.error(f"Error al eliminar el móvil con ID {id}: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    manager = DatabaseManagerObject()
    manager.conectar()
    try:
        # Inserta tres objetos
        manager.iniciar_transaccion()
        manager.crear_movil(1, "Galaxy S23", "Samsung", "Android", 8, 256)
        manager.crear_movil(2, "iPhone 14", "Apple", "iOS", 6, 128)
        manager.crear_movil(3, "Pixel 7", "Google", "Android", 8, 128)
        manager.confirmar_transaccion()

        # Muestra todos los objetos
        manager.leer_moviles()

        # Inserta un objeto con un ID ya creado
        manager.iniciar_transaccion()
        manager.crear_movil(1, "Galaxy S21", "Samsung", "Android", 8, 128)
        manager.revertir_transaccion()

        # Muestra todos los objetos
        manager.leer_moviles()

        # Actualiza un objeto
        manager.iniciar_transaccion()
        manager.actualizar_movil(2, "iPhone 14 Pro", "Apple", "iOS", 8, 256)
        manager.confirmar_transaccion()

        # Muestra todos los objetos
        manager.leer_moviles()

        # Elimina un objeto que no existe
        manager.iniciar_transaccion()
        manager.eliminar_movil(99)
        manager.revertir_transaccion()

        # Muestra todos los objetos
        manager.leer_moviles()
    except Exception as e:
        logging.error(f"Error general: {e}")
    finally:
        manager.desconectar()
