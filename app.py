import streamlit as st
import pandas as pd
import os
import re

from agent import IAAgent


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
    "ID_empleados",
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
                return row["ID_empleados"]

    return None


# =====================================================
# CONSTRUIR PAYLOAD
# =====================================================

def build_payload(empleado):

    # elimina NaN pero mantiene estructura original Excel

    return empleado.dropna().to_dict()


# =====================================================
# MOCK HISTORIAL (temporal)
# =====================================================

def fake_history():

    data = {
        "Empleado": [
            "EMP001","EMP023","EMP003","EMP013",
            "EMP001","EMP023","EMP001","EMP010",
            "EMP011","EMP012","EMP014","EMP015",
            "EMP016","EMP017","EMP018","EMP019"
        ],
        "Riesgo": [
            "ALTO","MEDIO","ALTO","MEDIO",
            "ALTO","MEDIO","BAJO","ALTO",
            "MEDIO","BAJO","ALTO","MEDIO",
            "BAJO","ALTO","MEDIO","BAJO"
        ],
        "Score": [
            "72%","45%","72%","45%",
            "90%","45%","20%","81%",
            "39%","22%","88%","47%",
            "15%","76%","41%","19%"
        ],
        "Fecha": [
            "2026-03-10","2026-03-10","2026-04-10","2026-04-10",
            "2026-04-10","2026-04-10","2026-05-10","2026-05-12",
            "2026-05-13","2026-05-14","2026-05-15","2026-05-16",
            "2026-05-17","2026-05-18","2026-05-19","2026-05-20"
        ]
    }

    return pd.DataFrame(data)


# =====================================================
# EJECUTAR PREDICCIÓN
# =====================================================

def ejecutar_prediccion(empleado):

    payload = build_payload(empleado)

    st.json(payload)  # DEBUG opcional

    # result = process(payload)
    result = print("Simulando proceso IA..." + payload)  # REEMPLAZA CON TU BACKEND REAL

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
                "Ejemplo: analiza Maria o EMP001"
            )

            if user_input:

                employee_id = extract_employee_id(
                    user_input,
                    df
                )

                if employee_id:

                    empleado = df[
                        df["ID_empleados"] == employee_id
                    ].iloc[0]

                    result = ejecutar_prediccion(
                        empleado
                    )

                    st.write(
                        "Probabilidad abandono:",
                        result["probabilidad"]
                    )

                    st.write(
                        "Nivel riesgo:",
                        result["riesgo"]
                    )

                    st.write(
                        "Recomendación:"
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

            if "Nombres" in df.columns:

                df["display_employee"] = (
                    df["ID_empleados"].astype(str)
                    + " - "
                    + df["Nombres"].astype(str)
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
                    df["ID_empleados"]
                )

            empleado = df[
                df["ID_empleados"] == employee_id
            ].iloc[0]

            st.subheader("Perfil empleado")

            if "Nombres" in df.columns:

                st.write(
                    "Nombre:",
                    empleado["Nombres"]
                )

            st.write(
                "Departamento:",
                empleado["departamento"]
            )

            st.write(
                "Tipo contrato:",
                empleado["tipo_contrato"]
            )

            if st.button("Ejecutar análisis"):

                result = ejecutar_prediccion(
                    empleado
                )

                st.metric(
                    "Probabilidad abandono",
                    result["probabilidad"]
                )

                st.write(
                    "Nivel riesgo:",
                    result["riesgo"]
                )

                st.write(
                    "Recomendación:"
                )

                st.info(
                    result["recomendacion"]
                )


# =====================================================
# HISTORIAL (SIN CAMBIOS)
# =====================================================

elif menu == "📁 Historial":

    st.header("Historial del agente")

    history = fake_history()

    # PAGINACIÓN

    rows_per_page = 10

    total_rows = len(history)

    total_pages = (total_rows // rows_per_page) + (
        total_rows % rows_per_page > 0
    )

    page = st.number_input(
        "Selecciona página",
        min_value=1,
        max_value=total_pages,
        step=1
    )

    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page

    paginated_df = history.iloc[start_idx:end_idx]

    st.dataframe(paginated_df, use_container_width=True)

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
        .astype(int)
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
# SIDEBAR REPORTE
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