import streamlit as st
import pandas as pd
import os
import re
import csv

import sqlite3
from datetime import datetime

from agent import IAAgent

# =====================================================
# CONEXIÓN BASE DE DATOS
# =====================================================
DB_PATH = "database/historial_consultas.db"


def init_historial_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial_consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        employee_name TEXT,
        risk_score TEXT,
        risk_level TEXT,
        recommendation TEXT,
        fecha TEXT
    )
    """)

    conn.commit()
    conn.close()


init_historial_db()

# =====================================================
# GUARDAR CONSULTA EN HISTORIAL
# =====================================================

def guardar_consulta(payload, result):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO historial_consultas (
            employee_id,
            employee_name,
            risk_score,
            risk_level,
            recommendation,
            fecha
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
    (
        payload["employee_id"],
        payload.get("employee_name", "N/A"),
        result["probabilidad"],
        result["riesgo"],
        result["recomendacion"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()

    conn.close()


# =====================================================
# GUARDAR CONSULTA EN CSV REPORTE
# =====================================================


def guardar_alerta_riesgo_alto(payload, result):

    if result["riesgo"].lower() != "alto":
        return

    os.makedirs("reports", exist_ok=True)

    file_path = "reports/reporte_riesgo_alto_empleados.csv"

    file_exists = os.path.isfile(file_path)

    # limpiar saltos de línea de la recomendación

    recomendacion_limpia = (
        result["recomendacion"]
        .replace("\n", " ")
        .replace("\r", " ")
        .strip()
    )

    with open(file_path, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "employee_id",
                "employee_name",
                "risk_score",
                "risk_level",
                "recommendation",
                "fecha"
            ])

        writer.writerow([
            payload["employee_id"],
            payload.get("employee_name", "N/A"),
            result["probabilidad"],
            result["riesgo"],
            recomendacion_limpia,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Agente Inteligente RRHH",
    layout="wide"
)


# =====================================================
# SIDEBAR MENU
# =====================================================

st.sidebar.image("assets/logo.png", width=200)

menu = st.sidebar.selectbox(
    "Selecciona el modo",
    [
        "💬 Chat IA",
        "📊 Análisis por empleado",
        "📁 Historial",
        "📈 Modelos predictivo"
    ]
)


# =====================================================
# VALIDAR DATASET
# =====================================================

required_columns = [
    "id_empleados",
    "employee_name",
    "edad",
    "salario",
    "experiencia",
    "departamento",
    "tipo_contrato",
    "horas_trabajo",
    "satisfaccion_laboral",
    "balance_trabajo_vida",
    "promociones",
    "distancia_trabajo",
    "comentarios_empleado"
]


def validate_dataset(df):

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    return missing


# =====================================================
# EXTRAER EMPLOYEE ID DESDE CHAT
# =====================================================

def extract_employee_id(text, df):

    text = text.lower()

    match = re.search(r"(emp\d+)", text)

    if match:
        return match.group(1).upper()

    if "Nombres" in df.columns:

        for _, row in df.iterrows():

            if str(row["Nombres"]).lower() in text:
                return row["id_empleados"]

    return None


# =====================================================
# CONSTRUIR PAYLOAD
# =====================================================

def build_payload(empleado):

    # elimina NaN pero mantiene estructura original Excel

    return empleado.dropna().to_dict()


# =====================================================
# EJECUTAR PREDICCIÓN
# =====================================================

def ejecutar_prediccion(empleado):

    payload = build_payload(empleado)

    payload["employee_id"] = payload["id_empleados"]

    if "employee_name" in payload:

        payload["employee_name"] = payload["employee_name"]

    agent = IAAgent()

    result_model = agent.analyze_employee_json(payload)

    result = {
        "probabilidad": f"{round(result_model['risk_score'] * 100, 2)}%",
        "riesgo": result_model["risk_level"],
        "recomendacion": result_model["recommendation"]
    }

    guardar_consulta(payload, result)

    guardar_alerta_riesgo_alto(payload, result)

    return result
# =====================================================
# CHAT IA
# =====================================================

if menu == "💬 Chat IA":

    st.header("Asistente Inteligente de Análisis")

    uploaded_file = st.file_uploader(
        "📄 Dataset empleados",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        missing_cols = validate_dataset(df)

        if missing_cols:

            st.error(
                f"Faltan columnas necesarias: {missing_cols}"
            )

        else:

            st.success("Dataset cargado correctamente")

            user_input = st.chat_input(
                "Ejemplo: analiza Johanna o EMP001"
            )

            if user_input:

                employee_id = extract_employee_id(
                    user_input,
                    df
                )

                if employee_id:

                    empleado = df[
                        df["id_empleados"] == employee_id
                    ].iloc[0]

                    result = ejecutar_prediccion(
                        empleado
                    )

                    if "employee_name" in df.columns:

                         st.write(
                          "👤 Nombre:",
                             empleado["employee_name"]
                         )

                    if "departamento" in df.columns:

                            st.write(
                                "🏢 Departamento:",
                                empleado["departamento"]
                            )
                    if "tipo_contrato" in df.columns:   

                            st.write(
                                "📄 Tipo contrato:",
                                empleado["tipo_contrato"]
                            )

                    st.write(
                        "🔎 Probabilidad abandono:",
                        result["probabilidad"]
                    )
                    
                    st.write(
                        "⚠️ Nivel riesgo:",
                        result["riesgo"]
                    )

                    st.write(
                      "📌Recomendación:"
                    )

                    st.info(
                        result["recomendacion"]
                    )

                else:

                    st.warning(
                        "Empleado no encontrado"
                    )


# =====================================================
# ANALISIS EMPLEADO
# =====================================================

elif menu == "📊 Análisis por empleado":

    st.header("Análisis Individual de Empleado")

    uploaded_file = st.file_uploader(
        "📄 Cargar dataset CSV",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        missing_cols = validate_dataset(df)

        if missing_cols:

            st.error(
                f"Faltan columnas necesarias: {missing_cols}"
            )

        else:

            st.success("Dataset válido")

            # SELECTOR INTELIGENTE ID + NOMBRE

            if "employee_name" in df.columns:

                df["display_employee"] = (
                    df["id_empleados"].astype(str)
                    + " - "
                    + df["employee_name"].astype(str)
                )

                selected_display = st.selectbox(
                    "Selecciona empleado",
                    df["display_employee"]
                )

                employee_id = selected_display.split(
                    " - "
                )[0]

            else:

                employee_id = st.selectbox(
                    "Selecciona empleado",
                    df["id_empleados"].astype(str)
                )

            empleado = df[
                df["id_empleados"].astype(str) == employee_id
            ].iloc[0]

            st.subheader("Perfil empleado")

            if "employee_name" in df.columns:

                st.write(
                    "👤 Nombre:",
                    empleado["employee_name"]
                )

            st.write(
                "🏢  Departamento:",
                empleado["departamento"]
            )

            st.write(
                "📄 Tipo contrato:",
                empleado["tipo_contrato"]
            )

            if st.button("Ejecutar análisis"):

                result = ejecutar_prediccion(
                    empleado
                )

                st.metric(
                    "🔎Probabilidad abandono",
                    result["probabilidad"]
                )

                st.write(
                    "⚠️ Nivel riesgo:",
                    result["riesgo"]
                )

                st.write(
                    "📌 Recomendación:"
                )

                st.info(
                    result["recomendacion"]
                )


# =====================================================
# HISTORIAL
# =====================================================

elif menu == "📁 Historial":

    st.header("Historial del agente")

    import sqlite3

    conn = sqlite3.connect(DB_PATH)

    history = pd.read_sql_query(
        """
        SELECT 
            employee_id AS "ID empleado",
            employee_name AS "Empleado",
            risk_level AS "Riesgo",
            risk_score AS "Score",
            fecha AS "Fecha"
        FROM historial_consultas
        ORDER BY fecha DESC
        """,
        conn
    )

    conn.close()

    # VALIDACIÓN SI NO HAY REGISTROS

    if history.empty:

        st.info("Aún no existen consultas registradas.")

    else:

        # PAGINACIÓN

        rows_per_page = 10

        total_rows = len(history)

        total_pages = (
            total_rows // rows_per_page
        ) + (total_rows % rows_per_page > 0)

        page = st.number_input(
            "Selecciona página",
            min_value=1,
            max_value=int(total_pages),
            step=1
        )

        start_idx = (page - 1) * rows_per_page
        end_idx = start_idx + rows_per_page

        paginated_df = history.iloc[start_idx:end_idx]

        st.dataframe(
            paginated_df,
            use_container_width=True
        )

        st.caption(
            f"Mostrando página {page} de {total_pages}"
        )
    # =====================================================
    # TRAZABILIDAD SCORE
    # =====================================================

    st.subheader("Trazabilidad del score por empleado")

    selected_employee = st.selectbox(
        "Selecciona empleado",
        history["Empleado"].unique()
    )

    employee_history = history[
        history["Empleado"] == selected_employee
    ].copy()

    employee_history["Score"] = (
        employee_history["Score"]
        .str.replace("%", "")
        .astype(float)
    )

    employee_history["Fecha"] = pd.to_datetime(
        employee_history["Fecha"]
    )

    employee_history = employee_history.sort_values(
        "Fecha"
    )

    st.line_chart(
        employee_history.set_index("Fecha")["Score"]
    )


    # =====================================================
    # FRECUENCIA RIESGO
    # =====================================================

    st.subheader("Frecuencia niveles riesgo")

    riesgo_counts = history["Riesgo"].value_counts()

    st.bar_chart(riesgo_counts)


# =====================================================
# MODELOS PREDICTIVOS
# =====================================================

elif menu == "📈 Modelos predictivo":
    st.header("Modelos Predictivos")

    if os.path.exists("models/plots/confusion_rf.png"):

        st.image("models/plots/confusion_rf.png")

    if os.path.exists("models/plots/confusion_xgb.png"):

        st.image("models/plots/confusion_xgb.png")


# =====================================================
# SIDEBAR REPORTE
# =====================================================

st.sidebar.divider()

st.sidebar.subheader("Reporte automático")

file_path = "reports/reporte_riesgo_alto_empleados.csv"

if os.path.exists(file_path):

    with open(file_path, "rb") as file:

        st.sidebar.download_button(
            "📥 Descargar reporte CSV",
            file,
            file_name="reporte_riesgo_alto_empleados.csv"
        )

else:

    st.sidebar.info(
        "Sin empleados en riesgo alto aún"
    )
