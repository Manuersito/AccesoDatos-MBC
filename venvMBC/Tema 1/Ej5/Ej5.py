import json

class JSONFileHandler:

 def write_json(self, file_path, content):
    try:
        with open(file_path, "w") as w:
            w.write(content)
    except Exception as e:
        print(f"Error escribiendo en el archivo: {e}")


 #Codigo para leer el json   
 def read_json(self, file_path):
     try:
         with open(file_path, 'r') as f:
             return json.load(f)
     except Exception as e:
         print(f"Error leyendo JSON: {e}")
# Uso
json_handler = JSONFileHandler()
content = {
    "DNI": "20065377",
    "fecha_de_nacimiento": "08/02/03"
}
#json.dumps lo que hace es pasar el diccionario a texto ya que el diccionario se
#interpreta como un objeto json
content_json = json.dumps(content)
json_handler.write_json("data.json", content_json)

data = json_handler.read_json('data.json')
print(data)
