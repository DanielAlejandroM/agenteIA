import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 10000


# 1. Generación de variables
edad = np.random.randint(18, 61, n)
experiencia = np.random.randint(0, 31, n)
antiguedad = np.minimum(experiencia, np.random.randint(0, 21, n))

salario = np.random.randint(482, 4001, n)
salario_base = np.random.randint(482, 2500, n)
salario = salario_base + experiencia * 50
salario = np.clip(salario, 482, 4000)

horas_trabajo = np.random.randint(30, 61, n)

satisfaccion = np.random.randint(1, 6, n)
work_life_balance = np.random.randint(1, 6, n)

promociones = np.random.randint(0, 6, n)
distancia = np.random.randint(0, 51, n)

departamentos = ["IT", "RRHH", "Ventas", "Finanzas", "Producción", "Logística"]
departamento = np.random.choice(departamentos, n)

tipo_contrato = np.random.choice(["temporal", "fijo"], n, p=[0.3, 0.7])


# 2. Función de probabilidad de renuncia
def calcular_prob(i):
    prob = 0.2  # base

    # salario bajo + baja satisfacción
    if salario[i] < 1200 and satisfaccion[i] <= 2:
        prob += 0.25

    # muchas horas
    if horas_trabajo[i] > 50:
        prob += 0.15

    # mal balance vida-trabajo
    if work_life_balance[i] <= 2:
        prob += 0.15

    # sin promociones
    if promociones[i] == 0:
        prob += 0.1

    # alta experiencia + promociones
    if experiencia[i] > 10 and promociones[i] >= 2:
        prob -= 0.15

    # buen salario + alta satisfacción
    if salario[i] > 2500 and satisfaccion[i] >= 4:
        prob -= 0.2

    # distancia alta
    if distancia[i] > 30:
        prob += 0.05

    # contrato temporal
    if tipo_contrato[i] == "temporal":
        prob += 0.05

    # ruido aleatorio
    # ruido gaussiano para evitar que el modelo aprenda reglas perfectas
    prob += np.random.normal(0, 0.05)

    # limita el ruido, probabilidades varias
    return np.clip(prob, 0, 1)


# 3. Generar target
probs = np.array([calcular_prob(i) for i in range(n)])
renuncia = np.random.binomial(1, probs)

# Esta parte es importante para no hacer al sistema determinista
# porque dos empleados con las mismas condiciones pueden tener distinto resultado


# 4. Ajustar distribución (~65/35)
target_ratio = 0.35
current_ratio = renuncia.mean()

if current_ratio < target_ratio:
    idx = np.where(renuncia == 0)[0]
    flip = np.random.choice(idx, size=int((target_ratio - current_ratio) * n), replace=False)
    renuncia[flip] = 1

elif current_ratio > target_ratio:
    idx = np.where(renuncia == 1)[0]
    flip = np.random.choice(idx, size=int((current_ratio - target_ratio) * n), replace=False)
    renuncia[flip] = 0


def generar_comentario(i):
    # Comentarios según nivel de satisfacción
    if satisfaccion[i] <= 2:  # Baja satisfacción
        opciones = [
            "Estoy muy insatisfecho con mi trabajo",
            "No me siento valorado en la empresa",
            "El ambiente laboral es muy malo",
            "Siento que mi esfuerzo no se reconoce",
            "El trabajo es estresante y agotador",
            "No tengo motivación para seguir aquí",
            "La carga de trabajo es abrumadora",
            "Siento que mis habilidades no se aprovechan",
            "Hay falta de comunicación en el equipo",
            "No recibo retroalimentación suficiente",
            "Mi jefe no apoya mi desarrollo profesional",
            "Los recursos para trabajar son insuficientes",
            "El ambiente de oficina es tenso",
            "No hay oportunidades de crecimiento",
            "Me siento sobrecargado y desmotivado"
        ]
    elif satisfaccion[i] >= 4:  # Alta satisfacción
        opciones = [
            "Estoy contento con mi trabajo",
            "Me gusta el ambiente laboral",
            "Estoy satisfecho con mi equipo",
            "Disfruto trabajar en esta empresa",
            "Mi equipo y mi jefe me apoyan mucho",
            "Estoy motivado y satisfecho con mis proyectos",
            "Siento que crezco profesionalmente",
            "Me siento reconocido por mis esfuerzos",
            "La cultura de la empresa es positiva",
            "Hay buenas oportunidades de aprendizaje",
            "Trabajo en proyectos que me interesan",
            "Tengo un equilibrio razonable entre trabajo y vida",
            "El liderazgo de mi equipo es excelente",
            "Me siento parte de un buen equipo",
            "Estoy orgulloso de lo que hacemos"
        ]
    else:  # Media satisfacción
        opciones = [
            "El trabajo es aceptable",
            "Hay cosas buenas y malas",
            "Mi experiencia es promedio",
            "Algunas tareas son interesantes, otras no tanto",
            "El equipo es bueno, pero la gestión necesita mejorar",
            "Estoy aprendiendo cosas nuevas, pero hay desafíos",
            "A veces me siento motivado, a veces no",
            "El ambiente es regular, podría mejorar",
            "Siento que mi esfuerzo no siempre se reconoce",
            "Tengo oportunidades limitadas para crecer",
            "Hay tareas repetitivas que no disfruto",
            "El equilibrio entre trabajo y vida es justo",
            "Me esfuerzo por mejorar en mi puesto",
            "Siento que algunos procesos son confusos",
            "Aprecio el apoyo de mis compañeros pero no siempre de mi jefe"
        ]

    # Elegir comentario al azar
    comentario = random.choice(opciones)

    # Agregar modificaciones según horas o salario
    if horas_trabajo[i] > 50:
        comentario += " y me siento muy estresado por la carga laboral"
    if salario[i] < 1000:
        comentario += " además considero que el salario es bajo"

    return comentario

comentarios = [generar_comentario(i) for i in range(n)]


# Limitar experiencia máxima a la edad del empleado
experiencia = np.minimum(experiencia, edad)

# 6. Crear DataFrame
df = pd.DataFrame({
    "edad": edad,
    "salario": salario,
    "experiencia": experiencia,
    "antiguedad_empresa": antiguedad,
    "departamento": departamento,
    "tipo_contrato": tipo_contrato,
    "horas_trabajo": horas_trabajo,
    "satisfaccion_laboral": satisfaccion,
    "work_life_balance": work_life_balance,
    "promociones": promociones,
    "distancia_trabajo": distancia,
    "comentarios_empleado": comentarios,
    "renuncia": renuncia
})

# 7. Guardar CSV
df.to_csv("empleados.csv", index=False)

# 8. Resumen básico
print(df.head())
print("\nDistribución de renuncia:")
print(df["renuncia"].value_counts(normalize=True))

print(df.head())

print("\nDistribución de renuncia:")
print(df["renuncia"].value_counts(normalize=True))

print("\nResumen estadístico:")
print(df.describe())

print("\nConteo de clases:")
print(df["renuncia"].value_counts())