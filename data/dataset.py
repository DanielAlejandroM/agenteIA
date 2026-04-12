import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

n = 10000


# Edad
edad = np.random.randint(18, 61, n)

# Experiencia (dependiente de edad)
# REGLA: la experiencia depende de la edad del empleado.
edad_inicio_trabajo = np.random.normal(22, 3, n).astype(int)
edad_inicio_trabajo = np.clip(edad_inicio_trabajo, 18, 30)

experiencia = edad - edad_inicio_trabajo

# REGLA: la experiencia no es continua (puede haber pausas)
pausas = np.random.binomial(1, 0.3, n) * np.random.randint(0, 5, n)
experiencia = experiencia - pausas
experiencia = np.clip(experiencia, 0, None)

# REGLA: no se puede tener mas antiguedad superar experiencia
antiguedad = np.array([
    np.random.randint(0, exp + 1) if exp > 0 else 0
    for exp in experiencia
])

# REGLA: a mayor experiencia -> mayor salario
salario_base = np.random.randint(482, 2000, n)
salario = salario_base + experiencia * np.random.randint(30, 80, n)
salario = np.clip(salario, 482, 4000)

# Horas de trabajo
horas_trabajo = np.random.randint(30, 61, n)

# REGLA: mas tiempo en la empresa -> mas oportunidades de ascenso
# promociones
promociones = np.array([
    np.random.randint(0, min(5, ant + 1))
    for ant in antiguedad
])

# REGLA: satisfacción (depende de condiciones laborales)
# satisfaccion
satisfaccion = np.array([
    np.clip(
        np.random.randint(2, 5)
        - (1 if horas_trabajo[i] > 50 else 0)
        - (1 if salario[i] < 1000 else 0)
        + (1 if promociones[i] > 1 else 0),
        1, 5
    )
    for i in range(n)
])

# 8. Work-life balance
work_life_balance = np.random.randint(1, 6, n)

# 9. Distancia
distancia = np.random.randint(0, 51, n)

# 10. Departamento
departamentos = ["ti", "rrhh", "ventas", "finanzas", "produccion", "logistica"]
departamento = np.random.choice(departamentos, n)

# 11. Tipo de contrato
tipo_contrato = np.random.choice(["temporal", "fijo"], n, p=[0.3, 0.7])

# REGLA: La renuncia depende de múltiples factores combinados
# Función de probabilidad de renuncia
def calcular_prob(i):
    prob = 0.2  # base

    # Factores que aumentan la probabilidad de renuncia

    # bajo salario + baja satisfacción
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

    # Factores que reducen la prob renuncia: experiencia + promociones
    if experiencia[i] > 10 and promociones[i] >= 2:
        prob -= 0.15

    # Factores que reducen la prob renuncia: buen salario + alta satisfacción
    if salario[i] > 2500 and satisfaccion[i] >= 4:
        prob -= 0.2

    # distancia alta
    if distancia[i] > 30:
        prob += 0.05

    # contrato temporal
    if tipo_contrato[i] == "temporal":
        prob += 0.05

    # ruido aleatorio (gaussiano) evita que el modelo aprenda reglas perfectas
    # REGLA: no determinista
    prob += np.random.normal(0, 0.05)

    # limita el ruido, probabilidades varias
    return np.clip(prob, 0, 1)


# Generar target
probs = np.array([calcular_prob(i) for i in range(n)])
renuncia = np.random.binomial(1, probs)



# Ajustar distribución (50/50)
target_ratio = 0.50
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
    prob = np.random.rand()

    # REGLA: el texto depende parcialmente de la satisfacción
    # 70% sigue lógica real, 30% introduce ruido
    if prob < 0.7:
        nivel = satisfaccion[i]
    else:
        nivel = np.random.randint(1, 6)

    # BAJA SATISFACCIÓN (15+)
    if nivel <= 2:
        opciones = [
            "estoy muy insatisfecho con mi trabajo",
            "no me siento valorado en la empresa",
            "el ambiente laboral es muy malo",
            "siento que mi esfuerzo no se reconoce",
            "el trabajo es estresante y agotador",
            "no tengo motivacion para seguir en este trabajo",
            "la carga de trabajo es abrumadora",
            "siento que mis habilidades no se aprovechan",
            "hay falta de comunicacion en el equipo",
            "no recibo retroalimentacion suficiente",
            "mi jefe no apoya mi desarrollo profesional",
            "los recursos para trabajar son insuficientes",
            "el ambiente de oficina es tenso",
            "no hay oportunidades de crecimiento",
            "me siento sobrecargado y desmotivado",
            "no confio en la direccion de la empresa",
            "siento que mi trabajo no tiene impacto",
            "el liderazgo es deficiente",
            "no hay reconocimiento al esfuerzo",
            "me siento estancado profesionalmente"
        ]

    # ALTA SATISFACCIÓN (15+)
    elif nivel >= 4:
        opciones = [
            "estoy contento con mi trabajo",
            "me gusta el ambiente laboral",
            "estoy satisfecho con mi equipo",
            "disfruto trabajar en esta empresa",
            "mi equipo y mi jefe me apoyan mucho",
            "estoy motivado y satisfecho con mis proyectos",
            "siento que crezco profesionalmente",
            "me siento reconocido por mis esfuerzos",
            "la cultura de la empresa es positiva",
            "hay buenas oportunidades de aprendizaje",
            "trabajo en proyectos que me interesan",
            "tengo un equilibrio razonable entre trabajo y vida",
            "el liderazgo de mi equipo es excelente",
            "me siento parte de un buen equipo",
            "estoy orgulloso de lo que hacemos",
            "siento estabilidad en mi trabajo",
            "mi desarrollo profesional es constante",
            "la empresa valora a sus empleados",
            "estoy satisfecho con las condiciones laborales",
            "hay un buen ambiente de colaboracion"
        ]

    # SATISFACCIÓN MEDIA (15+)
    else:
        opciones = [
            "el trabajo es aceptable",
            "hay cosas buenas y malas",
            "mi experiencia es promedio",
            "algunas tareas son interesantes, otras no tanto",
            "el equipo es bueno, pero la gestion necesita mejorar",
            "estoy aprendiendo cosas nuevas, pero hay desafios",
            "a veces me siento motivado, a veces no",
            "el ambiente es regular, podria mejorar",
            "siento que mi esfuerzo no siempre se reconoce",
            "tengo oportunidades limitadas para crecer",
            "hay tareas repetitivas que no disfruto",
            "el equilibrio entre trabajo y vida es justo",
            "me esfuerzo por mejorar en mi puesto",
            "siento que algunos procesos son confusos",
            "aprecio el apoyo de mis colegas pero no siempre de mi jefe",
            "el trabajo cumple con lo esperado",
            "no es el mejor trabajo, pero tampoco el peor",
            "hay estabilidad pero falta innovacion",
            "la empresa tiene potencial de mejora",
            "cumplo mis funciones sin mayor inconveniente"
        ]

    comentario = random.choice(opciones)

    # 🔥 FACTORES ADICIONALES (ruido realista)
    if horas_trabajo[i] > 50 and np.random.rand() < 0.5:
        comentario += " y me siento muy estresado por la carga laboral"

    if salario[i] < 1000 and np.random.rand() < 0.5:
        comentario += " ademas considero que el salario es bajo"

    if promociones[i] == 0 and np.random.rand() < 0.3:
        comentario += " y siento que no hay crecimiento profesional"

    return comentario
comentarios = [generar_comentario(i) for i in range(n)]


# Limitar experiencia máxima a la edad del empleado
experiencia = np.minimum(experiencia, edad)

# Crear DataFrame
df = pd.DataFrame({
    "edad": edad,
    "salario": salario,
    "experiencia": experiencia,
    "antiguedad_empresa": antiguedad,
    "departamento": departamento,
    "tipo_contrato": tipo_contrato,
    "horas_trabajo": horas_trabajo,
    "satisfaccion_laboral": satisfaccion,
    "balance_trabajo_vida": work_life_balance,
    "promociones": promociones,
    "distancia_trabajo": distancia,
    "comentarios_empleado": comentarios,
    "renuncia": renuncia
})

# guarda CSV
df.to_csv("empleados.csv", index=False)

# resumen básico
print(df.head())

print("\nDistribución de renuncia:")
print(df["renuncia"].value_counts(normalize=True))

print("\nResumen estadístico:")
print(df.describe())

print("\nConteo de clases:")
print(df["renuncia"].value_counts())

# validaciones
print("\nVALIDACIONES:")
print("Errores experiencia > edad:", (experiencia > (edad - 18)).sum())
print("Errores antigüedad > experiencia:", (antiguedad > experiencia).sum())
print("Valores negativos experiencia:", (experiencia < 0).sum())
print("Valores negativos antigüedad:", (antiguedad < 0).sum())