import pandas as pd

# Cambiar la configuración para mostrar todas las filas y columnas
pd.set_option('display.max_rows', None)  # Mostrar todas las filas
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
# Configurar pandas para mostrar números en formato normal
pd.options.display.float_format = '{:,.0f}'.format

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('used_car_dataset.csv')

# Mostrar el DataFrame
print("Imprimiendo shape:")
print(df.shape)
print("Imprimiendo head:")
print(df.head())
print("Imprimiendo info:")
print(df.info())
print("Imprimiendo describe:")
print(df.describe())
print("Imprimiendo 4 columnas:")
coches = df[["Brand", "model", "Year", "kmDriven"]]
print(coches.head())

# Limpieza de la columna AskPrice
df['AskPrice'] = df['AskPrice'].str.replace('₹', '', regex=False)  # Eliminar símbolo ₹
df['AskPrice'] = df['AskPrice'].str.replace(',', '', regex=False)  # Eliminar comas
df['AskPrice'] = pd.to_numeric(df['AskPrice'], errors='coerce')    # Convertir a numérico

# Limpieza de la columna kmDriven
df['kmDriven'] = df['kmDriven'].str.replace(' km', '', regex=False)  # Eliminar texto ' km'
df['kmDriven'] = df['kmDriven'].str.replace(',', '', regex=False)    # Eliminar comas
df['kmDriven'] = pd.to_numeric(df['kmDriven'], errors='coerce')      # Convertir a numérico

# Calcular precio por kilómetro
print("Imprimiendo precio por kilómetro:")
df["pricePerKm"] = df["AskPrice"] / df["kmDriven"]  # Crear la columna
print(df["pricePerKm"].head())

# Filtrar filas donde el año sea menor a 2015
filtered_df = df[df["Year"] < 2015]

# Mostrar las primeras 5 filas del DataFrame filtrado
print("Filas filtradas (Year < 2015):")
print(filtered_df.head())

# Eliminar filas con valores nulos
df_limpio = df.dropna() # Crear un nuevo DataFrame sin valores nulos
print(f"Filas antes: {df.shape[0]}")
print(f"Filas después: {df_limpio.shape[0]}")



# Filtrar filas donde "kmDriven" es nulo antes de rellenar los nulos
nulos_antes = df[df["kmDriven"].isna()]
print("Filas donde 'kmDriven' es nulo antes de rellenar:")
print(nulos_antes.head())

# Rellenar los valores nulos en "kmDriven" con 123
df["kmDriven"] = df["kmDriven"].fillna(123)


# Filtrar filas donde "kmDriven" es igual a 123 después de rellenar los nulos
filas_123 = df[df["kmDriven"] == 123]
print("Filas donde 'kmDriven' es igual a 123 después de rellenar:")
print(filas_123.head())




#Calcular promedio de marca y modelo
promedio_precio_por_marca_modelo = df.groupby(["Brand", "model"])[["AskPrice"]].mean()
print("Promedio del precio por marca y modelo:")
print(promedio_precio_por_marca_modelo)


