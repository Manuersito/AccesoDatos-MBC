import peewee
from peewee import IntegrityError, MySQLDatabase, Model, CharField

# Configurar la base de datos
db = MySQLDatabase(
    "1dam",  # Nombre de la base de datos
    user="usuario",  # Usuario de MySQL
    password="usuario",  # Contraseña de MySQL
    host="localhost",  # Host
    port=3306,  # Puerto por defecto de MySQL
)

# Conectar a la base de datos
db.connect()
print("Conexión exitosa a la base de datos.")


# Función para verificar si una tabla existe
def tabla_existe(nombre_tabla):
    consulta = """
    SELECT COUNT(*) FROM information_schema.tables 
    WHERE table_schema = %s AND table_name = %s
    """
    cursor = db.execute_sql(consulta, ("1dam", nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0


# Definir el modelo para la tabla 'Moviles'
class Moviles(Model):
    Marca = CharField()
    Modelo = CharField()
    Sistema_Operativo = CharField()
    Capacidad = CharField()
    Precio = CharField()
    Tienda_id = CharField()

    class Meta:
        database = db  # Base de datos
        table_name = "Moviles"  # Nombre de la tabla en la base de datos


try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        # TAREA 1: Recuperar objetos de un tipo específico
        print("Tarea1...")
        movilesAndroid = Moviles.select().where(Moviles.Sistema_Operativo == "Android")
    for movil in movilesAndroid:
        print(f"Marca: {movil.Marca}, Modelo: {movil.Modelo}")

except IntegrityError as e:
    print(f"Error al insertar herramientas: {e}")

try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        # TAREA 2: Eliminar un registro específico basado en dos atributos
        print("Tarea2...")
        movilEliminar = Moviles.get(
            Moviles.Marca == "Samsung", Moviles.Modelo == "Galaxy S21"
        )
        movilEliminar.delete_instance()  # Eliminar el registro
        print("Registro eliminado. Mostrando los registros restantes:")
        movilesRestantes = Moviles.select()
        for movil in movilesRestantes:
            print(f"Marca: {movil.Marca}, Modelo: {movil.Modelo}")

except IntegrityError as e:
    print(f"Error al insertar herramientas: {e}")

try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        # TAREA 3: Eliminar todos los registros que cumplan una condición
        print("Tarea3...")
        # Eliminar todos los registros que cumplan la condición
        Moviles.delete().where(Moviles.Precio > "800").execute()
        print("Registros eliminados. Mostrando los registros restantes:")
        movilesRestantes = Moviles.select()
        for movil in movilesRestantes:
            print(
                f"Marca: {movil.Marca}, Modelo: {movil.Modelo}, Precio: {movil.Precio}"
            )

except IntegrityError as e:
    print(f"Error al insertar herramientas: {e}")


# Cerrar la conexión a la base de datos
db.close()
print("Conexión a la base de datos cerrada.")
