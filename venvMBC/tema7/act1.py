import pandas as pd

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