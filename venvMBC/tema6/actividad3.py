import logging
from peewee import Model, CharField, ForeignKeyField, MySQLDatabase

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("databasemanager_orm.log"),
        logging.StreamHandler()
    ]
)

# Configuración de la base de datos MySQL
db = MySQLDatabase(
    "1dam",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306  # Puerto por defecto de MySQL
)

# Modelos de la base de datos
class Proveedor(Model):
    nombre = CharField()
    direccion = CharField()

    class Meta:
        database = db


class Herramienta(Model):
    nombre = CharField()
    tipo = CharField()
    marca = CharField()
    uso = CharField()
    material = CharField()
    proveedor = ForeignKeyField(Proveedor, backref='herramientas')

    class Meta:
        database = db


# Componente DatabaseManagerORM
class DatabaseManagerORM:
    def __init__(self):
        self.db = db

    def conectar(self):
        """Conecta la base de datos y crea las tablas."""
        self.db.connect()
        self.db.create_tables([Proveedor, Herramienta])
        logging.info("Conexión establecida y tablas creadas.")

    def desconectar(self):
        """Cierra la conexión a la base de datos."""
        if not self.db.is_closed():
            self.db.close()
            logging.info("Conexión cerrada.")

    def iniciar_transaccion(self):
        """Inicia una transacción."""
        self.db.begin()
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        """Confirma (commit) una transacción."""
        self.db.commit()
        logging.info("Transacción confirmada.")

    def revertir_transaccion(self):
        """Revierte (rollback) una transacción."""
        self.db.rollback()
        logging.info("Transacción revertida.")

    def crear_proveedor(self, nombre, direccion):
        """Inserta un nuevo proveedor."""
        proveedor = Proveedor.create(nombre=nombre, direccion=direccion)
        logging.info(f"Proveedor creado: {proveedor.nombre} - {proveedor.direccion}")
        return proveedor

    def actualizar_proveedor(self, proveedor, nueva_direccion):
        """Actualiza la dirección de un proveedor."""
        proveedor.direccion = nueva_direccion
        proveedor.save()
        logging.info(f"Proveedor actualizado: {proveedor.nombre} - {proveedor.direccion}")

    def eliminar_proveedor(self, proveedor):
        """Elimina un proveedor."""
        nombre = proveedor.nombre
        proveedor.delete_instance()
        logging.info(f"Proveedor eliminado: {nombre}")

    def crear_herramienta(self, nombre, tipo, marca, uso, material, proveedor):
        """Inserta una nueva herramienta."""
        herramienta = Herramienta.create(
            nombre=nombre, tipo=tipo, marca=marca, uso=uso, material=material, proveedor=proveedor
        )
        logging.info(f"Herramienta creada: {herramienta.nombre} - {herramienta.tipo}")
        return herramienta

    def actualizar_herramienta(self, herramienta, nuevo_tipo):
        """Actualiza el tipo de una herramienta."""
        herramienta.tipo = nuevo_tipo
        herramienta.save()
        logging.info(f"Herramienta actualizada: {herramienta.nombre} - {herramienta.tipo}")

    def eliminar_herramienta(self, herramienta):
        """Elimina una herramienta."""
        nombre = herramienta.nombre
        herramienta.delete_instance()
        logging.info(f"Herramienta eliminada: {nombre}")

    def leer_herramientas_por_proveedor(self, proveedor):
        """Lee todas las herramientas de un proveedor."""
        herramientas = Herramienta.select().where(Herramienta.proveedor == proveedor)
        logging.info(f"Herramientas asociadas al proveedor {proveedor.nombre}:")
        for herramienta in herramientas:
            logging.info(f"{herramienta.nombre} - {herramienta.tipo}")
        return herramientas


# Ejecución de la actividad
if __name__ == "__main__":
    manager = DatabaseManagerORM()
    manager.conectar()

    # Gestión de Proveedores
    manager.iniciar_transaccion()
    proveedor_a = manager.crear_proveedor("Proveedor A", "Contacto 123-456-789")
    proveedor_b = manager.crear_proveedor("Proveedor B", "Contacto 987-654-321")
    manager.confirmar_transaccion()

    # Actualizar Proveedor A
    manager.iniciar_transaccion()
    manager.actualizar_proveedor(proveedor_a, "20065377Q")  # DNI
    manager.confirmar_transaccion()

    # Eliminar Proveedor B
    manager.iniciar_transaccion()
    manager.eliminar_proveedor(proveedor_b)
    manager.confirmar_transaccion()

    # Gestión de Herramientas
    manager.iniciar_transaccion()
    martillo = manager.crear_herramienta("Martillo", "Manual", "Marca1", "Uso1", "Acero", proveedor_a)
    taladro = manager.crear_herramienta("Taladro", "Eléctrico", "Marca2", "Uso2", "Metal", proveedor_a)
    manager.confirmar_transaccion()

    # Leer herramientas asociadas a Proveedor A
    manager.leer_herramientas_por_proveedor(proveedor_a)

    # Actualizar Martillo
    manager.iniciar_transaccion()
    manager.actualizar_herramienta(martillo, "Reforzado")
    manager.confirmar_transaccion()

    # Eliminar Taladro
    manager.iniciar_transaccion()
    manager.eliminar_herramienta(taladro)
    manager.confirmar_transaccion()

    manager.desconectar()
