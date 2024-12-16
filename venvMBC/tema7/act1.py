import pandas as pd

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('tema7/used_car_dataset.csv')

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
print("Imprimiendo precio por kilómetro:")
df["pricePerKm"] = df["AskPrice"]/df["kmDriven"]
print(df["pricePerrKm"].head())
