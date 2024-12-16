from peewee import MySQLDatabase
from peewee import Model, CharField, IntegerField,PrimaryKeyField,AutoField

import ZODB
import transaction
from ZODB import FileStorage, DB
from persistent import Persistent

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


# Definir el autor para la tabla 'Libros'
class Libros(Model):
    id = IntegerField(),PrimaryKeyField(),AutoField()
    titulo = CharField(100)
    autor = CharField(100)
    anio_publicacion = IntegerField()
    genero = CharField(50)

    class Meta:
        database = db  # Base de datos
        table_name = "Libros"  # Nombre de la tabla en la base de datos


# Crear la tabla si no existe
db.create_tables([Libros])
print("Tabla 'Libros' creada o ya existente.")

# Insertar registros en la tabla 'Libros'
Libros.create(
    titulo="Cien años de soledad",
    autor="Gabriel García Márquez",
    anio_publicacion= 1967,
    genero="Novela"
)
Libros.create(
    titulo="Don Quijote de la Mancha",
    autor="Miguel de Cervantes",
    anio_publicacion= 1605,
    genero="Novela"
    
)
Libros.create(
    titulo="El Principito",
    autor="Antoine de Saint-Exupéry",
    anio_publicacion= 1943,
    genero="Infantil"
    
)
Libros.create(
    titulo="Crónica de una muerte anunciada",
    autor="Gabriel García Márquez",
    anio_publicacion= 1981,
    genero="Novela"
)
Libros.create(
    titulo="1984",
    autor="George Orwell",
    anio_publicacion= 1949,
    genero="Distopía"
)

print("Registros insertados exitosamente.")

# Cerrar la conexión a la base de datos
db.close()
print("Conexión a la base de datos cerrada.")






print("Base de datos ZODB")
class Prestamo(Persistent):
    def __init__(self, libro_id, nombre_usuario, fecha_prestamo, fecha_devolucion):
        self.libro_id = libro_id
        self.nombre_usuario = nombre_usuario
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

# Configuración de la base de datos
storage = FileStorage.FileStorage('Prestamo.fs')
dbz = DB(storage)
connectionz = dbz.open()
root = connectionz.root

print("Conexion abierta")
# Inicializa la raíz si está vacía
if not hasattr(root, 'Prestamo'):
    root.Prestamo = {}

# Almacenar varios objetos Libros
try:
    def almacenar_Prestamo():
        usuario1 = Prestamo(1, 'Juan Perez', '2023-10-01', '2023-11-01')
        usuario2 = Prestamo(2, 'Ana Lopez', '2023-09-15', '2023-10-15')
        usuario3 = Prestamo(4, 'Maria Gomez', '2023-09-20', '2023-10-20')

        # Almacenar los móviles en la base de datos
        root.Prestamo['usuario1'] = usuario1
        root.Prestamo['usuario2'] = usuario2
        root.Prestamo['usuario3'] = usuario3

        # Confirmar los cambios
        transaction.commit()
except Exception as e:
    transaction.abort()
    print(f"Error durante la transacción: {e}. Transacción revertida.")

# Consultar objetos Libros
def consultar_Libros(libro_id):
    if libro_id == "null":
        print("No hay prestamos asociados")
    else:
        print(f"Libros con genero Novela:")
        for key in root.Prestamo.keys():
            Libros = root.Prestamo[key]
            # Verifica si el objeto tiene el atributo 'fecha_prestamo' y filtra
            if hasattr(Prestamo, 'fecha_prestamo') and Prestamo.libro_id == libro_id:
                print(f"Libro: {Libros.titulo}, nombre_usuario: {Prestamo.nombre_usuario}, fecha_prestamo: {Prestamo.fecha_prestamo}, fecha_devolucio: {Prestamo.fecha_devolucion}")

def buscar_prestamos_por_genero(generos):
    db.connect
    if generos != "Novela":
        print("El genero no existe")
    else :
        Libros_novelas = Libros.select().where(Libros.genero == generos)
        consultar_Libros(Libros.id)
    db.close
    

# Función principal
def main():
    almacenar_Prestamo()
    buscar_prestamos_por_genero("Novela")

# Ejecuta el programa
if __name__ == "__main__":
    main()

    # Cierra la conexión
    connectionz.close()
    dbz.close()
print("Conexion zodb cerrada")