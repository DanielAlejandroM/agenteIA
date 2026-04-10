import pandas as pd

# cargar el dataset previamente guardado
df = pd.read_csv("empleados.csv")

# validación del dataset
def validar_dataset(df):
    print("🔹 Primeras filas:")
    print(df.head(), "\n")
    print("🔹 Información general:")
    print(df.info(), "\n")
    print("🔹 Estadísticas básicas:")
    print(df.describe(), "\n")
    print("🔹 Distribución de renuncia:")
    print(df["renuncia"].value_counts(normalize=True), "\n")

    # Revisar experiencia <= edad
    if (df["experiencia"] > df["edad"]).any():
        print("Atención: empleados con experiencia > edad")
        print(df[df["experiencia"] > df["edad"]])
    else:
        print("Todos los valores de experiencia son ≤ edad")

    # rangos
    for col, min_val, max_val in [
        ("edad", 18, 60), ("salario", 482, 4000), ("experiencia", 0, 30),
        ("antiguedad_empresa", 0, 20), ("horas_trabajo", 30, 60),
        ("satisfaccion_laboral", 1, 5), ("work_life_balance", 1, 5),
        ("promociones", 0, 5), ("distancia_trabajo", 0, 50)
    ]:
        if df[col].between(min_val, max_val).all():
            print(f"{col} dentro de rango")
        else:
            print(f"{col} fuera de rango")

    # prom. x renuncia
    print("\n🔹 Promedios por renuncia (ver patrones):")
    print(df.groupby("renuncia")[["salario","satisfaccion_laboral","horas_trabajo","promociones"]].mean())
    print("\nChecklist completado: si todo está OK, dataset listo para ML")


validar_dataset(df)