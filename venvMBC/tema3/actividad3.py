import peewee
from peewee import IntegrityError,MySQLDatabase, Model, CharField

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
    cursor = db.execute_sql(consulta, ('1dam', nombre_tabla))
    resultado = cursor.fetchone()
    return resultado[0] > 0




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

# Verificar si la tabla 'Moviles' existe y eliminarla si es necesario
if tabla_existe(Moviles._meta.table_name):
    print(f"La tabla '{Moviles._meta.table_name}' existe.")
    db.drop_tables([Moviles], cascade=True)
    print(f"Tabla '{Moviles._meta.table_name}' eliminada con éxito.")
else:
    print(f"La tabla '{Moviles._meta.table_name}' no existe.")

# Crear la tabla si no existe
db.create_tables([Moviles])
print("Tabla 'Moviles' creada o ya existente.")


try:
    # Iniciar una transacción utilizando db.atomic()
    with db.atomic():
        # Insertar registros en la tabla 'Moviles'
        Moviles.create(
        Marca="Samsung",
        Modelo="Galaxy S21",
        Sistema_Operativo="Android",
        Capacidad="128GB",
        Precio="799",
        Tienda_id="1",
        )
        Moviles.create(
        Marca="Apple",
        Modelo="iPhone 13",
        Sistema_Operativo="iOS",
        Capacidad="256GB",
        Precio="999",
        Tienda_id="1",
        )
        Moviles.create(
        Marca="Xiaomi",
        Modelo="Mi 11",
        Sistema_Operativo="Android",
        Capacidad="128GB",
        Precio="699",
        Tienda_id="1",
        )
        Moviles.create(
        Marca="OnePlus",
        Modelo="9 Pro",
        Sistema_Operativo="Android",
        Capacidad="256GB",
        Precio="899",
        Tienda_id="1",
        )
        Moviles.create(
        Marca="Google",
        Modelo="Pixel 6",
        Sistema_Operativo="Android",
        Capacidad="128GB",
        Precio="599",
        Tienda_id="1",
        )
    print("Moviles insertados correctamente.")
except IntegrityError as e:
    print(f"Error al insertar herramientas: {e}")

movilesRestantes = Moviles.select()
for movil in movilesRestantes:
    print(f"Marca: {movil.Marca}, Modelo: {movil.Modelo}, Precio: {movil.Precio}")
# Cerrar la conexión a la base de datos
db.close()
print("Conexión a la base de datos cerrada.")