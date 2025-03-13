import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv("used_car_dataset.csv")

# Preprocesamiento de datos
df["AskPrice"] = df["AskPrice"].str.replace("₹", "").str.replace(",", "").astype(float)
df["kmDriven"] = df["kmDriven"].str.replace(" km", "").str.replace(",", "").astype(float)
df["Transmission"] = df["Transmission"].map({"Manual": 0, "Automatic": 1})
df = pd.get_dummies(df, columns=["Brand", "model"], drop_first=True)
df["Age"] = 2025 - df["Year"]
df = df.dropna(subset=["Age", "kmDriven", "Transmission", "AskPrice"])

# División de datos (80% entrenamiento, 20% prueba)
X = df[["Age", "kmDriven", "Transmission"]]
y = df["AskPrice"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### 1. REGRESIÓN LINEAL SIMPLE ###
model_lr_simple = LinearRegression()
model_lr_simple.fit(X_train[["Age"]], y_train)

y_pred_simple = model_lr_simple.predict(X_test[["Age"]])
rmse_simple = np.sqrt(mean_squared_error(y_test, y_pred_simple))
print(f"RMSE de Regresión Lineal Simple: {rmse_simple:.2f}")

# Seleccionar 30 coches equidistantes
num_samples = min(30, len(y_test))
indices = np.linspace(0, len(y_test) - 1, num_samples, dtype=int)

# Gráfico

plt.figure(figsize=(10,5))
plt.plot(range(len(indices)), y_test.iloc[indices], marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(range(len(indices)), y_pred_simple[indices], marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice del Coche")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión Lineal Simple - Comparación de Predicciones")
plt.legend()
plt.grid(True)
plt.show()

### 2. REGRESIÓN LINEAL MÚLTIPLE ###
model_lr_multi = LinearRegression()
model_lr_multi.fit(X_train, y_train)

y_pred_multi = model_lr_multi.predict(X_test)
rmse_multi = np.sqrt(mean_squared_error(y_test, y_pred_multi))
print(f"RMSE de Regresión Lineal Múltiple: {rmse_multi:.2f}")

# Gráfico

plt.figure(figsize=(10,5))
plt.plot(range(len(indices)), y_test.iloc[indices], marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(range(len(indices)), y_pred_multi[indices], marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice del Coche")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión Lineal Múltiple - Comparación de Predicciones")
plt.legend()
plt.grid(True)
plt.show()

### 3. REGRESIÓN XGBOOST ###
model_xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model_xgb.fit(X_train, y_train)

y_pred_xgb = model_xgb.predict(X_test)
rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
print(f"RMSE de Regresión XGBoost: {rmse_xgb:.2f}")

# Gráfico
plt.figure(figsize=(10,5))
plt.plot(range(len(indices)), y_test.iloc[indices], marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(range(len(indices)), y_pred_xgb[indices], marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice del Coche")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión XGBoost - Comparación de Predicciones")
plt.legend()
plt.grid(True)
plt.show()

### 4. REGRESIÓN XGBOOST CON TRATAMIENTO DE VALORES ERRÓNEOS ###
kmin, kmax = df["kmDriven"].quantile([0.01, 0.99])
df_filtered = df[(df["kmDriven"] >= kmin) & (df["kmDriven"] <= kmax)]

X_filtered = df_filtered[["Age", "kmDriven", "Transmission"]]
y_filtered = df_filtered["AskPrice"]
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=42)

model_xgb_filtered = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model_xgb_filtered.fit(X_train_f, y_train_f)

y_pred_filtered = model_xgb_filtered.predict(X_test_f)
rmse_filtered = np.sqrt(mean_squared_error(y_test_f, y_pred_filtered))
print(f"RMSE de Regresión XGBoost con Tratamiento de Valores Erróneos: {rmse_filtered:.2f}")

# Asegurar que los índices no sean mayores al tamaño del conjunto de prueba corregido
num_samples = min(30, len(y_test_f))
indices = np.linspace(0, len(y_test_f) - 1, num_samples, dtype=int)

plt.figure(figsize=(10,5))
plt.plot(range(len(indices)), y_test_f.iloc[indices], marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(range(len(indices)), y_pred_filtered[indices], marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice del Coche")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión XGBoost (Con Valores Corregidos) - Comparación de Predicciones")
plt.legend()
plt.grid(True)
plt.show()
