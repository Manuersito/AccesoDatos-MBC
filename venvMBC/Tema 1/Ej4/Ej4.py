import csv
import json

class FileConverter:
    def json_to_csv(self, json_file, csv_file):
        try:
            # Abrir el archivo JSON
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Obtener los encabezados del primer elemento
            headers = data[0].keys()
            
            # Abrir el archivo CSV para escritura
            with open(csv_file, 'w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                csv_writer.writeheader()
                
                # Escribir cada fila del JSON en el CSV
                for row in data:  # Cambiar 'json' a 'data'
                    csv_writer.writerow(row)

            print(f'Conversión de {json_file} a {csv_file} completada.')
        
        except Exception as e:
            print(f"Error en la conversión: {e}")

# Uso
converter = FileConverter()
converter.json_to_csv('data.json', 'data.csv')
