import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from sklearn.feature_extraction.text import TfidfVectorizer

# matriz de confusión
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# carga dataset
df = pd.read_csv("empleados.csv")

print(df.head())

# definir variables -- variable objetivo 
y = df["renuncia"]

# Variables numéricas
numericas = [
    "edad", "salario", "experiencia", "antiguedad_empresa",
    "horas_trabajo", "satisfaccion_laboral",
    "work_life_balance", "promociones", "distancia_trabajo"
]

# Variables categóricas
categoricas = ["departamento", "tipo_contrato"]

# Variable de texto
texto_col = "comentarios_empleado"

# procesar variables categóricas
cat_encoded = pd.get_dummies(df[categoricas])
# procesar texto pln
tfidf = TfidfVectorizer(max_features=100)
texto_vectorizado = tfidf.fit_transform(df[texto_col])

# unir todo -- crea el dataset final para el modelo
X = pd.concat([
    df[numericas].reset_index(drop=True),
    cat_encoded.reset_index(drop=True),
    pd.DataFrame(texto_vectorizado.toarray())
], axis=1)

X.columns = X.columns.astype(str)

# dividir datos en 80% entrenamiento y 20% prueba 
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# entrenar el modelo
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# evaluar el modelo
y_pred = modelo.predict(X_test)

print(classification_report(y_test, y_pred))

# matriz de confusión
# matriz de confusión
cm = confusion_matrix(y_test, y_pred)

print("\nMatriz de Confusión:")
print(cm)

# visualizacion de la matriz
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap="Blues")
plt.title("Matriz de Confusión")
plt.show()


# ==============================
# FUNCIÓN DEL AGENTE (RAZONAMIENTO)
# ==============================

def analizar_empleado(datos_empleado):
    
    print("\n=== ANÁLISIS DEL AGENTE ===")
    
    # 1. CONTEXTO
    print("\n[1] Analizando contexto del empleado...")
    print(f"Edad: {datos_empleado['edad']}")
    print(f"Salario: {datos_empleado['salario']}")
    print(f"Satisfacción laboral: {datos_empleado['satisfaccion_laboral']}")
    print(f"Horas de trabajo: {datos_empleado['horas_trabajo']}")
    
    # 2. PATRONES
    print("\n[2] Identificando patrones...")
    if datos_empleado["salario"] < 1000:
        print("Patrón detectado: salario bajo")
    if datos_empleado["satisfaccion_laboral"] < 4:
        print("Patrón detectado: baja satisfacción laboral")
    if datos_empleado["horas_trabajo"] > 50:
        print("Patrón detectado: alta carga laboral")
    
    # 3. PREPARAR DATOS
    nuevo_df = pd.DataFrame([datos_empleado])
    
    nuevo_cat = pd.get_dummies(nuevo_df[categoricas])
    nuevo_cat = nuevo_cat.reindex(columns=cat_encoded.columns, fill_value=0)
    
    nuevo_texto = tfidf.transform(nuevo_df[texto_col])
    nuevo_texto_df = pd.DataFrame(nuevo_texto.toarray())
    
    nuevo_X = pd.concat([
        nuevo_df[numericas].reset_index(drop=True),
        nuevo_cat.reset_index(drop=True),
        nuevo_texto_df.reset_index(drop=True)
    ], axis=1)
    
    nuevo_X.columns = X.columns
    
    # 4. PREDICCIÓN
    prob = modelo.predict_proba(nuevo_X)[0][1]
    print(f"\n[3] Probabilidad de renuncia: {prob:.2f}")
    
    # 5. DECISIÓN
    if prob > 0.7:
        decision = "ALTO RIESGO"
    elif prob > 0.4:
        decision = "RIESGO MEDIO"
    else:
        decision = "RIESGO BAJO"
    
    print(f"[4] Decisión del agente: {decision}")
    
    return decision


# ==============================
# PRUEBA DEL AGENTE
# ==============================

empleado_prueba = {
    "edad": 30,
    "salario": 800,
    "experiencia": 3,
    "antiguedad_empresa": 2,
    "horas_trabajo": 55,
    "satisfaccion_laboral": 3,
    "work_life_balance": 4,
    "promociones": 0,
    "distancia_trabajo": 20,
    "departamento": "Ventas",
    "tipo_contrato": "Tiempo completo",
    "comentarios_empleado": "Estoy cansado del trabajo y no estoy satisfecho"
}

analizar_empleado(empleado_prueba)
