#diagramas de líneas, de dispersión, de barras,
#histograma y diagrama de cajas

import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("used_car_dataset.csv")

# Limpieza de la columna AskPrice
df['AskPrice'] = df['AskPrice'].str.replace('₹', '', regex=False)  # Eliminar símbolo ₹
df['AskPrice'] = df['AskPrice'].str.replace(',', '', regex=False)  # Eliminar comas
df['AskPrice'] = pd.to_numeric(df['AskPrice'], errors='coerce')    # Convertir a numérico

# Limpieza de la columna kmDriven
df['kmDriven'] = df['kmDriven'].str.replace(' km', '', regex=False)  # Eliminar texto ' km'
df['kmDriven'] = df['kmDriven'].str.replace(',', '', regex=False)    # Eliminar comas
df['kmDriven'] = pd.to_numeric(df['kmDriven'], errors='coerce')      # Convertir a numérico

# Agrupar por año y calcular el precio promedio
df_grouped = df.groupby('Year')['AskPrice'].mean().reset_index()

# Graficar la tendencia de precios por año del vehículo
plt.figure(figsize=(10, 6))
plt.plot(df_grouped['Year'], df_grouped['AskPrice'], marker='o', linestyle='-')

# Etiquetas y título
plt.xlabel("Año del Vehículo")
plt.ylabel("Precio Promedio (INR)")
plt.title("Tendencia de Precios por Año del Vehículo")
plt.grid(True)
plt.show()


# Graficar la relación entre Año del Vehículo y Kilometraje
plt.figure(figsize=(10, 5))
plt.scatter(df['Year'], df['kmDriven'], alpha=0.6, color='blue')

# Etiquetas y título
plt.xlabel("Año del Vehículo")
plt.ylabel("Kilometraje Recorrido")
plt.title("Relación entre Año del Vehículo y Kilometraje")
plt.grid(True)
plt.show()




# Crear gráfico de barras para mostrar el precio en función del kilometraje

# Crear una nueva columna 'kmGroup' para agrupar los kilometrajes en rangos de 25K km
bins = list(range(0, 1000001, 25000))  # Rangos de 25K km desde 0 hasta 1,000,000
labels = [f'{i}-{i+25000}K km' for i in range(0, 1000000, 25000)]  # Etiquetas de los rangos

df['kmGroup'] = pd.cut(df['kmDriven'], bins=bins, labels=labels, right=False)

# Agrupar por 'kmGroup' y calcular el precio promedio para cada rango de kilometraje
grouped = df.groupby('kmGroup')['AskPrice'].mean()

# Crear gráfico de barras para mostrar el precio promedio por rango de kilometraje
plt.figure(figsize=(12,6))
grouped.plot(kind='bar', color='lightblue')

# Añadir títulos y etiquetas
plt.title('Precio Promedio por Rango de Kilometraje', fontsize=14)
plt.xlabel('Rango de Kilometraje', fontsize=12)
plt.ylabel('Precio Promedio (₹)', fontsize=12)

# Mostrar gráfico
plt.xticks(rotation=90, ha='center')  # Rotar las etiquetas del eje X para mejor legibilidad
plt.tight_layout()  # Ajustar el diseño para evitar que las etiquetas se corten
plt.show()



# Crear histograma de precios (AskPrice)
plt.figure(figsize=(10,6))
plt.hist(df['AskPrice'], bins=10, color='skyblue', edgecolor='black')

# Añadir títulos y etiquetas
plt.title('Distribución de Precios de los Coches', fontsize=14)
plt.xlabel('Precio (₹)', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)

# Mostrar gráfico
plt.tight_layout()  # Ajustar el diseño para evitar que las etiquetas se corten
plt.show()






# Verificar si existen valores nulos y mostrarlos
print(df.isnull().sum())

# Eliminar filas con valores nulos en 'Year'
df = df.dropna(subset=['Year'])

# Crear diagrama de cajas de los años (Year)
plt.figure(figsize=(8,6))

# Asegurarse de que los datos de 'Year' sean numéricos
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

# Graficar el boxplot
plt.boxplot(df['Year'], vert=False, patch_artist=True, notch=True, 
            boxprops=dict(facecolor='lightblue', color='black'), 
            whiskerprops=dict(color='black'))

# Añadir títulos y etiquetas
plt.title('Distribución de Años de los Coches', fontsize=14)
plt.xlabel('Año', fontsize=12)

# Mostrar gráfico
plt.tight_layout()  # Ajustar diseño
plt.show()