import pymysql
import csv
import json



conexion = pymysql.connect(
        host='localhost',
        user='usuario',
        password='usuario',
        database='1dam'
    )


print("Conexión a la base de datos exitosa")
cursor = conexion.cursor()
cursor.execute("""
    CREATE TABLE if not exists Libros (
    id int AUTO_INCREMENT PRIMARY KEY,
    titulo varchar(50),
    autor varchar(50),
    genero varchar(50),
    año_publicacion varchar(50),
    libreria_origen varchar(50))
    """)        
print("Tabla creada correctamente")

print("\n")

class JSONFileHandler:
    def read_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error leyendo JSON: {e}")
        

class CSVFileHandler:
    def read_csv(self, file_path):
        try:
            with open(file_path, mode='r', newline='') as f:
                reader = csv.DictReader(f)
                rows = [] # Lista vacía para almacenar las filas
                for row in reader: # Recorremos cada fila en el archivo CSV
                    rows.append(row) # Añadimos cada fila (un diccionario) a la lista
            return rows # Devolvemos la lista con todas las filas
        except Exception as e:
            print(f"Error leyendo el archivo CSV: {e}")



json_handler = JSONFileHandler()       
data = json_handler.read_json('libros_machado.json')
print(data)
print("\n","\n")
csv_handler = CSVFileHandler()
contenido_csv = csv_handler.read_csv('libros_unamuno.csv')
print("Contenido del archivo CSV:")
print(contenido_csv)

libros_iniciales = [
        {"titulo": "Don Quijote de la Mancha", "autor": "Miguel de Cervantes", "genero": "Novela", "año_publicacion": 1605, "libreria_origen": "Ramón Valle Inclán"},
        {"titulo": "Cien Años de Soledad", "autor": "Gabriel García Márquez", "genero": "Novela", "año_publicacion": 1967, "libreria_origen": "Ramón Valle Inclán"},
        {"titulo": "Crimen y Castigo", "autor": "Fiódor Dostoyevski", "genero": "Novela", "año_publicacion": 1866, "libreria_origen": "Ramón Valle Inclán"},
        {"titulo": "La Casa de los Espíritus", "autor": "Isabel Allende", "genero": "Novela", "año_publicacion": 1982, "libreria_origen": "Ramón Valle Inclán"},
        {"titulo": "El Nombre de la Rosa", "autor": "Umberto Eco", "genero": "Misterio", "año_publicacion": 1980, "libreria_origen": "Ramón Valle Inclán"}
    ]


for i in libros_iniciales:
    sql_insert = """
    INSERT INTO Libros (titulo, autor, genero, año_publicacion, libreria_origen)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insert, (i["titulo"], i["autor"], i["genero"], i["año_publicacion"], i["libreria_origen"]))

for i in data:
    sql_insert = """
    INSERT INTO Libros (titulo, autor, genero, año_publicacion, libreria_origen)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insert, (i["titulo"], i["autor"], i["genero"], i["año_publicacion"], i["libreria_origen"]))

for i in contenido_csv:
    sql_insert = """
    INSERT INTO Libros (titulo, autor, genero, año_publicacion, libreria_origen)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql_insert, (i["titulo"], i["autor"], i["genero"], i["año_publicacion"], i["libreria_origen"]))
conexion.commit()  # Hacer commit una vez al final del bucle
print("Libros insertados correctamente en la base de datos")
    
        
    



