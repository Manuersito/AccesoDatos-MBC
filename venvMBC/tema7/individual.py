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
df = df.drop(columns=["FuelType", "Owner", "PostedDate", "AdditionInfo"], errors='ignore')
df["Age"] = 2025 - df["Year"]
df = df.dropna(subset=["Age", "kmDriven", "Transmission", "AskPrice"])

# Filtrar un rango de datos específico para visualización
df_sample = df[(df["Year"] >= 2015) & (df["Year"] <= 2020)]

### 1. REGRESIÓN LINEAL SIMPLE ###
X_simple = df_sample[["Age"]]
y_simple = df_sample["AskPrice"]
X_train_simple, X_test_simple, y_train_simple, y_test_simple = train_test_split(X_simple, y_simple, test_size=0.2, random_state=42)

model_lr_simple = LinearRegression()
model_lr_simple.fit(X_train_simple, y_train_simple)

y_pred_simple = model_lr_simple.predict(X_test_simple)
rmse_simple = np.sqrt(mean_squared_error(y_test_simple, y_pred_simple))
print(f"RMSE de Regresión Lineal Simple: {rmse_simple:.2f}")

plt.figure(figsize=(10,5))
plt.plot(X_test_simple, y_test_simple, marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(X_test_simple, y_pred_simple, marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Edad del Auto")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión Lineal Simple - Edad vs Precio (2015-2020)")
plt.legend()
plt.grid(True)
plt.show()

### 2. REGRESIÓN LINEAL MÚLTIPLE CON 3 VARIABLES ###
X_multi = df_sample[["Age", "kmDriven", "Transmission"]]
y_multi = df_sample["AskPrice"]
X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(X_multi, y_multi, test_size=0.2, random_state=42)

model_lr_multi = LinearRegression()
model_lr_multi.fit(X_train_multi, y_train_multi)

y_pred_multi = model_lr_multi.predict(X_test_multi)
rmse_multi = np.sqrt(mean_squared_error(y_test_multi, y_pred_multi))
print(f"RMSE de Regresión Lineal Múltiple con 3 variables: {rmse_multi:.2f}")

plt.figure(figsize=(10,5))
plt.plot(X_test_multi.index, y_test_multi, marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(X_test_multi.index, y_pred_multi, marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice de Datos")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión Lineal Múltiple - Comparación de Predicciones (2015-2020)")
plt.legend()
plt.grid(True)
plt.show()

### 3. REGRESIÓN XGBOOST ###
X_xgb = df_sample[["Age", "kmDriven", "Transmission"]]
y_xgb = df_sample["AskPrice"]
X_train_xgb, X_test_xgb, y_train_xgb, y_test_xgb = train_test_split(X_xgb, y_xgb, test_size=0.2, random_state=42)

model_xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model_xgb.fit(X_train_xgb, y_train_xgb)

y_pred_xgb = model_xgb.predict(X_test_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test_xgb, y_pred_xgb))
print(f"RMSE de Regresión XGBoost: {rmse_xgb:.2f}")

plt.figure(figsize=(10,5))
plt.plot(X_test_xgb.index, y_test_xgb, marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(X_test_xgb.index, y_pred_xgb, marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice de Datos")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión XGBoost - Comparación de Predicciones (2015-2020)")
plt.legend()
plt.grid(True)
plt.show()

### 4. REGRESIÓN XGBOOST CON TRATAMIENTO DE VALORES ERRÓNEOS ###
amin, amax = df_sample["Age"].quantile([0.01, 0.99])
kmin, kmax = df_sample["kmDriven"].quantile([0.01, 0.99])
df_filtered = df_sample[(df_sample["Age"] >= amin) & (df_sample["Age"] <= amax) & (df_sample["kmDriven"] >= kmin) & (df_sample["kmDriven"] <= kmax)]

X_filtered = df_filtered[["Age", "kmDriven", "Transmission"]]
y_filtered = df_filtered["AskPrice"]
X_train_f, X_test_f, y_train_f, y_test_f = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=42)

model_xgb_filtered = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model_xgb_filtered.fit(X_train_f, y_train_f)

y_pred_filtered = model_xgb_filtered.predict(X_test_f)
rmse_filtered = np.sqrt(mean_squared_error(y_test_f, y_pred_filtered))
print(f"RMSE de Regresión XGBoost con Tratamiento de Valores Erróneos: {rmse_filtered:.2f}")

plt.figure(figsize=(10,5))
plt.plot(X_test_f.index, y_test_f, marker='o', linestyle='-', color='blue', label="Datos reales")
plt.plot(X_test_f.index, y_pred_filtered, marker='x', linestyle='--', color='orange', label="Predicción")
plt.xlabel("Índice de Datos")
plt.ylabel("Precio del Auto (₹)")
plt.title("Regresión XGBoost (Con Valores Corregidos) - Comparación de Predicciones (2015-2020)")
plt.legend()
plt.grid(True)
plt.show()
