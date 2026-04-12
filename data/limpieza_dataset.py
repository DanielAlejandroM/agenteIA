import pandas as pd
import unicodedata
import re
import os

# Limpiar texto
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

# Carga del dataset
ruta = os.path.join(os.path.dirname(__file__), "empleados.csv")
df = pd.read_csv(ruta, encoding="utf-8")

# Limpieza
# RL: eliminar duplicados
df = df.drop_duplicates()
# RL: eliminar valores nulos
df = df.dropna()

# Validacion de rangos
df = df[(df["edad"] >= 18) & (df["edad"] <= 60)]
# experiencia vs edad
df = df[df["experiencia"] <= (df["edad"] - 18)]
# antiguedad vs experiencia
df = df[df["antiguedad_empresa"] <= df["experiencia"]]
df = df[(df["salario"] >= 482) & (df["salario"] <= 4000)]
# variables ordinales
df = df[(df["satisfaccion_laboral"] >= 1) & (df["satisfaccion_laboral"] <= 5)]
df = df[(df["balance_trabajo_vida"] >= 1) & (df["balance_trabajo_vida"] <= 5)]

df = df[(df["horas_trabajo"] >= 30) & (df["horas_trabajo"] <= 60)]
df = df[df["promociones"] >= 0]

# Limpieza texto nuevo (columnas tipo texto)
for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].apply(limpiar_texto)


df = df.reset_index(drop=True)

# Resumen

print("\nINFO DATASET:")
df.info()

print("\nDISTRIBUCIÓN TARGET:")
print(df["renuncia"].value_counts(normalize=True))

# Guardar archivo limpio
df.to_csv("empleados_limpio.csv", index=False, encoding="utf-8")
