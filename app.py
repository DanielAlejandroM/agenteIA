import streamlit as st
import pandas as pd
import os
import re

# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

st.set_page_config(
    page_title="Agente Inteligente RRHH",
    layout="wide"
)

# =====================================================
# HEADER PROFESIONAL (LOGO IZQUIERDA)
# =====================================================
# =====================================================
#col_logo, col_title = st.columns([1,6])

#with col_logo:
#    st.image("assets/logo.png", width=90)

#with col_title:
#    st.markdown(
#        """
#        <h1 style="margin-bottom:0;">
#        Agente Inteligente de Riesgo de Abandono Laboral
#        </h1>
#        <p style="margin-top:0; color:gray;">
#        Sistema de apoyo a decisiones basado en IA para Recursos Humanos
#        </p>
#        """,
#        unsafe_allow_html=True
#    )

# =====================================================
# SIDEBAR MENU
# =====================================================

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
# MOCK MODELO
# =====================================================

def fake_prediction():

    return {
        "probabilidad": "72%",
        "riesgo": "ALTO",
        "recomendacion": "Revisar carga laboral y salario"
    }

# =====================================================
# MOCK HISTORIAL
# =====================================================

def fake_history():

    data = {
        "Empleado": ["EMP001", "EMP023","EMP003", "EMP013","EMP001", "EMP023","EMP001"],
        "Riesgo": ["ALTO", "MEDIO","ALTO", "MEDIO","ALTO", "MEDIO","BAJO"],
        "Score": ["72%", "45%", "72%", "45%", "90%", "45%","20%"],
        "Recomendación": [
            "Revisar carga laboral y salario", "Fomentar desarrollo profesional", "Revisar carga laboral y salario", "Fomentar desarrollo profesional", "Revisar carga laboral y salario", "Fomentar desarrollo profesional", "Mantener seguimiento y reconocimiento"
        ],
        "Fecha": ["2026-03-10", "2026-03-10", "2026-04-10", "2026-04-10", "2026-04-10", "2026-04-10", "2026-05-10"]
    }

    return pd.DataFrame(data)

# =====================================================
# VALIDAR DATASET
# =====================================================

required_columns = [
    "ID_empleados",
    "edad",
    "salario",
    "experiencia",
    "departamento",
    "tipo_contrato",
    "horas_trabajo",
    "satisfaccion_laboral",
    "work_life_balance",
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
# EXTRAER EMPLOYEE ID DESDE TEXTO CHAT
# =====================================================

def extract_employee_id(text):

    match = re.search(r"(EMP\d+)", text.upper())

    if match:
        return match.group(1)

    return None


# =====================================================
# CHAT IA
# =====================================================

if menu == "💬 Chat IA":

    st.header("Asistente Inteligente de Análisis")

    uploaded_file = st.file_uploader(
        "📄 Dataset empleados",
        type=["csv"]
    )

    dataset_loaded = False

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        missing_cols = validate_dataset(df)

        if missing_cols:

            st.error(
                f"Faltan columnas necesarias: {missing_cols}"
            )

        else:

            dataset_loaded = True

            st.success("Dataset cargado correctamente")

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """
Hola 👋

Soy tu asistente de análisis predictivo.

Puedes escribir:

➡ analiza EMP001
➡ riesgo EMP023
"""
            }
        ]

    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

    user_input = st.chat_input(
        "Ejemplo: analiza EMP001"
    )

    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        with st.chat_message("user"):

            st.markdown(user_input)

        if not dataset_loaded:

            respuesta = """
⚠️ Primero debes cargar un dataset CSV para poder analizar empleados.
"""

        else:

            employee_id = extract_employee_id(user_input)

            if employee_id is None:

                respuesta = """
No detecté un ID válido.

Ejemplo correcto:

analiza EMP001
"""

            elif employee_id not in df["ID_empleados"].values:

                respuesta = f"""
El empleado **{employee_id}** no existe en el dataset cargado.
"""

            else:

                result = fake_prediction()

                respuesta = f"""
🔎 Resultado del análisis para **{employee_id}**

Probabilidad abandono: **{result["probabilidad"]}**

Nivel riesgo: **{result["riesgo"]}**

📌 Recomendación:

{result["recomendacion"]}
"""

        with st.chat_message("assistant"):

            st.markdown(respuesta)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": respuesta
            }
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

            employee_id = st.selectbox(
                "Selecciona empleado",
                df["ID_empleados"]
            )

            empleado = df[
                df["ID_empleados"] == employee_id
            ].iloc[0]

            st.subheader("Perfil empleado")

            if "Nombres" in df.columns:

                st.write("👤 Nombre:", empleado["Nombres"])

            else:

                st.warning(
                    "La columna 'Nombres' no está en el dataset"
                )

            st.write("🏢 Departamento:", empleado["departamento"])

            st.write("📄 Tipo contrato:", empleado["tipo_contrato"])

            if st.button("Ejecutar análisis"):

                result = fake_prediction()

                st.metric(
                    "Probabilidad abandono",
                    result["probabilidad"]
                )

                st.write("Nivel riesgo:", result["riesgo"])

                st.write("Recomendación:", result["recomendacion"])


# =====================================================
# HISTORIAL
# =====================================================

elif menu == "📁 Historial":

    st.header("Historial del agente")

    history = fake_history()

    st.dataframe(history)

    # =====================================================
    # TRAZABILIDAD DEL SCORE POR EMPLEADO
    # =====================================================

    st.subheader("Trazabilidad del score por empleado")

    # selector empleado

    selected_employee = st.selectbox(
        "Selecciona empleado para visualizar evolución",
        history["Empleado"].unique()
    )

    # filtrar empleado seleccionado

    employee_history = history[
        history["Empleado"] == selected_employee
    ].copy()

    # convertir Score de texto "72%" a número 72

    employee_history["Score"] = (
        employee_history["Score"]
        .str.replace("%", "")
        .astype(int)
    )

    # convertir fecha a formato datetime

    employee_history["Fecha"] = pd.to_datetime(
        employee_history["Fecha"]
    )

    # ordenar cronológicamente

    employee_history = employee_history.sort_values(
        "Fecha"
    )

    # graficar evolución

    st.line_chart(
        employee_history.set_index("Fecha")["Score"]
    )


# =====================================================
# REPORTE SIDEBAR
# =====================================================

st.sidebar.divider()

st.sidebar.subheader("Reporte automático")

if os.path.exists(
    "reports/reporte_riesgo_empleados.csv"
):

    with open(
        "reports/reporte_riesgo_empleados.csv",
        "rb"
    ) as file:

        st.sidebar.download_button(
            "📥 Descargar reporte CSV",
            file,
            file_name="reporte_riesgo_empleados.csv"
        )

else:

    st.sidebar.info(
        "Sin empleados en riesgo alto aún"
    )