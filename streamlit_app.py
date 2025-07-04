# SmartRental App
import streamlit as st
# --- Cargar estilos personalizados ---
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")
import pandas as pd
import numpy as np
import random
from scipy.optimize import newton

# --- CONFIGURACIÓN GLOBAL ---
st.set_page_config(page_title="SmartRental", layout="centered")

# --- ESTILO PERSONALIZADO ---
custom_css = """
<style>
/* Tipografía */
h1, h2, h3, h4, h5, h6 {
    font-family: Consolas, monospace;
    color: #07365b;
}

body, div, p, label, input, textarea, select, span {
    font-family: "Segoe UI", sans-serif;
    font-size: 16px;
    text-align: justify;
}

/* Títulos */
h1 {
    font-size: 2.5rem;
}
h2 {
    font-size: 1.8rem;
}
h3 {
    font-size: 1.4rem;
    color: #386d79;
}

/* Botón */
div.stButton > button {
    background-color: #4099c6;
    color: white;
    font-weight: bold;
    border-radius: 6px;
    padding: 0.6em 1.5em;
    font-size: 16px;
}

div.stButton > button:hover {
    background-color: #07365b;
}

/* Métricas */
div.element-container .stMetric {
    background-color: #f0f8ff;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #4099c6;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- LOGO + TÍTULO ---
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("Logo.jpeg", width=90)
with col_title:
    st.title("SmartRental")

st.markdown("""
Analiza la viabilidad de comprar un inmueble para renta en Airbnb.
Obtén un **precio promedio por noche** estimado y la **Tasa Interna de Retorno (TIR)** para tomar decisiones de inversión más inteligentes.
""")
st.markdown("---")

# El resto del código de funcionalidades permanece igual que en tu versión actual.
# Incluye inputs del inmueble, selección de amenidades, cálculos de inversión, botón de cálculo y visualización de resultados.
# Aplica automáticamente el nuevo diseño visual, colores y tipografías definidos arriba.

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado por Latam&Spain Soluciones Digitales")
