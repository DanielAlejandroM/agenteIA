import streamlit as st
import pandas as pd
from agent import predict_employee
from database import get_history

st.set_page_config(page_title="Agente IA RRHH")

menu = st.sidebar.selectbox(
    "Seleccionar modo",
    ["Chat IA", "Análisis por empleado", "Historial"]
)

print("Hello")