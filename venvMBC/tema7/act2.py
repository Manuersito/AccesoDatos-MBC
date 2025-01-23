import pandas as pd
from sklearn.model_selection import train_test_split
# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv("used_car_dataset.csv")


# Limpieza de la columna AskPrice
df['AskPrice'] = df['AskPrice'].str.replace('₹', '', regex=False)  # Eliminar símbolo ₹
df['AskPrice'] = df['AskPrice'].str.replace(',', '', regex=False)  # Eliminar comas
df['AskPrice'] = pd.to_numeric(df['AskPrice'], errors='coerce')    # Convertir a numérico

# Limpieza de la columna kmDriven
df['kmDriven'] = df['kmDriven'].str.replace(' km', '', regex=False)  # Eliminar texto ' km'
df['kmDriven'] = df['kmDriven'].str.replace(',', '', regex=False)    # Eliminar comas
df['kmDriven'] = pd.to_numeric(df['kmDriven'], errors='coerce')      # Convertir a numérico


#Calcular el rango intercuartil (IQR)
q1 = df["AskPrice"].quantile(0.25) # Primer cuartil
print("Primer cuartil")
print(q1)
q3 = df["AskPrice"].quantile(0.75) # Tercer cuartil
print("Tercer cuartil")
print(q3)
iqr = q3 - q1 # Rango intercuartil
print("Rango intercuartil")
print(iqr)
# Definir los límites inferior y superior
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
print(f"Límite inferior: {lower_bound}, Límite superior: {upper_bound}")
# Filtrar valores dentro de los límites
df_sin_atipicos = df[(df["AskPrice"] >= lower_bound) & (df["AskPrice"] <=
upper_bound)]
# Comparar el número de filas antes y después
print(f"Filas antes: {df.shape[0]}")
print(f"Filas después de eliminar atípicos: {df_sin_atipicos.shape[0]}")

print("")
print("")
print("")
# Calcular la media y la desviación estándar de las columnas
mean_km = df["kmDriven"].mean()
std_km = df["kmDriven"].std()
print(f" Media de km recorridos:{mean_km}")
print(f" Desviación estándar km recorridos:{std_km}")

# Estandarizar las columnas
df["kmDriven_z"] = (df["kmDriven"] - mean_km) / std_km

# Mostrar los resultados
print("Columnas originales y estandarizadas:")
print(df[["kmDriven", "kmDriven_z"]].head())

print("")
print("")
print("")

# Aplicar one-hot encoding a la columna 'Brand'
df_one_hot = pd.get_dummies(df, columns=['Brand'], prefix='Brand')

# Mostrar las primeras filas del dataframe resultante, incluyendo solo las columnas de marcas
print(df_one_hot.filter(like='Brand_').head())


pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
# Aplicar one-hot encoding a la columna 'Brand'
df_one_hot1 = pd.get_dummies(df, columns=['model'], prefix='Model')
print(df_one_hot1.filter(like='Model_').head())

print("")
print("")
print("")


# Variables predictoras
X = df[["Brand", "model", "Year", "kmDriven","Transmission","Owner","FuelType"]]
# Variable objetivo
y = df["AskPrice"]

X = pd.get_dummies(X, columns=["Brand", "model", "Year", "kmDriven","Transmission","Owner","FuelType"],
drop_first=True)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
random_state=42)
# Mostrar resultados
print("Tamaño del conjunto de entrenamiento:", X_train.shape[0])
print("Tamaño del conjunto de prueba:", X_test.shape[0])

print("")
print("")
print("")

def calcular_media(columna):
    return columna.mean()
# Aplicar la función a cada columna (axis=0)
medias = df[["Year", "kmDriven"]].apply(calcular_media, axis=0)
# Mostrar el resultado
print("\nMedias de las columnas 'Year' y 'kmDriven':")
print(medias)
