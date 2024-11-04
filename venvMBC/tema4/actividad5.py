from ZODB import DB, FileStorage
from persistent import Persistent
import ZODB
import transaction


storage = FileStorage.FileStorage('moviles3.fs')
db = DB(storage)
connection = db.open()
root = connection.root()

# Clases para movil y tienda

class Movil(Persistent):
    def __init__(self, marca, modelo, anio_lanzamiento, sistema_operativo, tienda):
        self.marca = marca
        self.modelo = modelo
        self.anio_lanzamiento = anio_lanzamiento
        self.sistema_operativo = sistema_operativo
        self.tienda = tienda
        
        
class Tienda(Persistent):
    def __init__(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion
# Verificar y crear colecciones si no existen



if 'movil' not in root:
    root['movil'] = {}
if 'tienda' not in root:
    root['tienda'] = {}
# Insertar datos en Proveedores
root['tienda']['mediamarkt'] = Tienda("mediamarkt", "cc. los alcores")
root['tienda']['phonehouse'] = Tienda("phonehouse", "cc. nervion")
# Insertar datos en Herramientas, incluyendo id_proveedor
root['movil']['Xiaomi'] = Movil("Xiaomi", "mi11", "2020", "android",
"mediamarkt")
root['movil']['Iphone'] = Movil("Iphone", "16 pro", "2024", "IOS",
"phonehouse")
root['movil']['Samsung'] = Movil("Samsubg", "galaxy", "2018", "android",
"mediamarkt")
transaction.commit()

# Filtrar e imprimir los móviles con sistema operativo Android
for nombre, movil in root['movil'].items():
    if movil.sistema_operativo == "android":
        print(f"Marca: {movil.marca}, Modelo: {movil.modelo}, Año de lanzamiento: {movil.anio_lanzamiento}, Sistema operativo: {movil.sistema_operativo}, Tienda: {movil.tienda}")

# Cerrar conexión
connection.close()
db.close()