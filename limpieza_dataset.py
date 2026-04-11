import pandas as pd
import unicodedata
import re
import os

# -------------------------------
# FUNCIÓN PARA LIMPIAR TEXTO
# -------------------------------
def limpiar_texto(texto):
    if isinstance(texto, str):
        # Pasar a minúsculas
        texto = texto.lower()
        
        # Quitar tildes
        texto = unicodedata.normalize('NFD', texto)
        texto = texto.encode('ascii', 'ignore').decode('utf-8')
        
        # Eliminar caracteres raros (solo letras y números)
        texto = re.sub(r'[^a-z0-9\s]', '', texto)
        
        # Quitar espacios extra
        texto = re.sub(r'\s+', ' ', texto).strip()
        
    return texto

# -------------------------------
# 1. Cargar dataset (buffer reader)
# -------------------------------
ruta = os.path.join(os.path.dirname(__file__), "data", "empleados.csv")
df = pd.read_csv(ruta, encoding="utf-8")

# -------------------------------
# 2. LIMPIEZA ORIGINAL
# -------------------------------

df = df.drop_duplicates()
df = df.dropna()

df = df[(df["edad"] >= 18) & (df["edad"] <= 60)]
df = df[df["experiencia"] <= (df["edad"] - 18)]
df = df[df["antiguedad_empresa"] <= df["experiencia"]]
df = df[(df["salario"] >= 482) & (df["salario"] <= 4000)]

df = df[(df["satisfaccion_laboral"] >= 1) & (df["satisfaccion_laboral"] <= 5)]
df = df[(df["balance_trabajo_vida"] >= 1) & (df["balance_trabajo_vida"] <= 5)]

df = df[(df["horas_trabajo"] >= 30) & (df["horas_trabajo"] <= 60)]
df = df[df["promociones"] >= 0]

# -------------------------------
# 3. LIMPIEZA DE TEXTO (NUEVO)
# -------------------------------

# Aplicar solo a columnas tipo texto
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].apply(limpiar_texto)

# -------------------------------
# Resetear índice
# -------------------------------
df = df.reset_index(drop=True)

# -------------------------------
# 4. RESUMEN
# -------------------------------

print("\nINFO DATASET:")
df.info()

print("\nDISTRIBUCIÓN TARGET:")
print(df["renuncia"].value_counts(normalize=True))

# -------------------------------
# 5. Guardar dataset limpio
# -------------------------------
df.to_csv("empleados_limpio.csv", index=False, encoding="utf-8")
