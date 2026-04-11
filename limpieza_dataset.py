import pandas as pd

# 1. Cargar dataset
df = pd.read_csv("empleados.csv")

# 2. LIMPIEZA

# Eliminar duplicados
df = df.drop_duplicates()

# Eliminar nulos
df = df.dropna()

# Validar rangos
df = df[(df["edad"] >= 18) & (df["edad"] <= 60)]

# Validar experiencia
df = df[df["experiencia"] <= (df["edad"] - 18)]

# Validar antigüedad
df = df[df["antiguedad_empresa"] <= df["experiencia"]]

# Validar salario
df = df[(df["salario"] >= 482) & (df["salario"] <= 4000)]

# Validar variables ordinales
df = df[(df["satisfaccion_laboral"] >= 1) & (df["satisfaccion_laboral"] <= 5)]
df = df[(df["work_life_balance"] >= 1) & (df["work_life_balance"] <= 5)]

# Validar horas
df = df[(df["horas_trabajo"] >= 30) & (df["horas_trabajo"] <= 60)]

# Validar promociones
df = df[df["promociones"] >= 0]

# Resetear índice
df = df.reset_index(drop=True)

# 3. RESUMEN

print("\nINFO DATASET:")
df.info()

print("\nDISTRIBUCIÓN TARGET:")
print(df["renuncia"].value_counts(normalize=True))
