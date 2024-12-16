from ZODB import DB, FileStorage
from persistent import Persistent
import ZODB
import transaction
import copy

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

moviloriginal = root['movil']['Iphone']
movilcopia = copy.deepcopy(moviloriginal)

movilcopia.sistema_operativo = "Android raro"
transaction.commit
#movil original
print("Movil original")
print(f"Marca: {moviloriginal.marca}, Modelo: {moviloriginal.modelo}, Año de lanzamiento: {moviloriginal.anio_lanzamiento}, Sistema operativo: {moviloriginal.sistema_operativo}, Tienda: {moviloriginal.tienda}")

#movil copia
print("Movil copia")
print(f"Marca: {movilcopia.marca}, Modelo: {movilcopia.modelo}, Año de lanzamiento: {movilcopia.anio_lanzamiento}, Sistema operativo: {movilcopia.sistema_operativo}, Tienda: {movilcopia.tienda}")


# Cerrar conexión
connection.close()
db.close()