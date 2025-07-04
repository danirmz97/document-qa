# app.py

import streamlit as st
import pandas as pd
import numpy as np
import random
from scipy.optimize import newton

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(layout="centered", page_title="SmartRental")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #ffffff;
        color: #07365b;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Consolas', monospace;
        color: #07365b;
    }

    .stButton > button {
        background-color: #386d79;
        color: white;
        border: none;
        padding: 0.5em 1.5em;
        font-size: 16px;
        border-radius: 8px;
    }

    .stButton > button:hover {
        background-color: #4099c6;
        color: white;
    }

    .stMarkdown, .stCaption, .stText, .stSubheader, .stHeader, .stTitle, .stDataFrame {
        text-align: justify;
    }

    .stMetric {
        font-size: 20px;
    }

    </style>
""", unsafe_allow_html=True)

# --- CONSTANTES ---
CIUDADES_DISPONIBLES = ["Barcelona", "Madrid", "Valencia", "Málaga", "Sevilla"]  # Acortado para demo
costos_operacion_porcentaje = .5
ocupacion_anual_porcentaje = .70
tasa_descuento_objetivo = .10
horizonte_analisis_anos = 10

def get_random_price(min_price=50, max_price=300):
    return random.uniform(min_price, max_price)

def npv_function(tir_guess, flujos):
    npv = 0
    for i, flujo in enumerate(flujos):
        npv += flujo / (1 + tir_guess)**i
    return npv

def calculate_irr(cash_flows):
    try:
        irr = newton(lambda r: npv_function(r, cash_flows), 0.10)
        return irr
    except RuntimeError:
        st.warning("No se pudo encontrar una TIR. Esto puede ocurrir si los flujos de caja son inconsistentes (ej. todos positivos o todos negativos después de la inversión).")
        return None
    except ZeroDivisionError:
        st.warning("Error matemático al calcular la TIR. Verifique los flujos de caja.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al calcular la TIR: {e}")
        return None

# --- TÍTULO Y LOGO ---
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.image("Logo.jpeg", width=100)
with col_title:
    st.title("SmartRental")

st.markdown("""
Analiza la viabilidad de comprar un inmueble para renta en Airbnb. Obtendrás un **precio promedio por noche** y la **Tasa Interna de Retorno (TIR)** estimada. Finalmente, la **Alerta de recomendación** para la compra o no del inmueble.
""")
st.markdown("---")

# --- 1. DATOS DEL INMUEBLE ---
st.header("1. Datos del Inmueble")

ciudad = st.multiselect("Ubicación (ciudad):", options=CIUDADES_DISPONIBLES, default=["Barcelona"], max_selections=1)
room_type = st.selectbox("Tipo de alojamiento:", ["Piso entero", "Habitación privada"])
numero_personas = st.slider("Número de huéspedes:", 1, 20, 4)
bathrooms = st.number_input("Número de baños:", 1.0, 10.0, step=0.5, value=1.0)
bedrooms = st.number_input("Número de dormitorios:", 1, 10, value=2)
beds = st.number_input("Número de camas:", 1, 20, value=3)
min_nights = st.number_input("Estancia mínima (noches):", 1, 365, value=2)
max_nights = st.number_input("Estancia máxima (noches):", min_nights, 365, value=30)

# --- 2. SELECCIÓN DE AMENIDADES ---
st.header("2. Selección de amenidades")

categorias = ["Confort", "Tecnología", "Cocina"]
amenities_por_categoria = {
    "Confort": ["aire acondicionado", "calefacción"],
    "Tecnología": ["wifi", "tv"],
    "Cocina": ["cafetera", "microondas"]
}

amenities_seleccionadas = {}

for categoria in categorias:
    if st.checkbox(categoria):
        seleccionadas = st.multiselect(f"Seleccione amenidades en {categoria}:", amenities_por_categoria[categoria])
        amenities_seleccionadas[categoria] = seleccionadas

# --- 3. COSTES DE INVERSIÓN ---
st.header("3. Costes de inversión")

inversion_inmueble = st.number_input("Inversión inicial del inmueble:", 10000.0, value=150000.0, step=1000.0)
inversion_amueblar = st.number_input("Inversión en amueblar y equipar:", 0.0, value=20000.0, step=500.0)
inversion_costes_admin = st.number_input("Costes administrativos anuales:", 0.0, value=5000.0, step=500.0)

st.markdown("---")

# --- BOTÓN PARA CALCULAR ---
if st.button("🚀 Calcular Precio y Rentabilidad"):
    st.header("4. Resultados SmartRental")

    precio_promedio_noche = get_random_price()
    st.subheader("Precio promedio por noche estimado:")
    st.metric("Precio Estimado", f"€{precio_promedio_noche:,.2f}")
    st.info("🚨 Nota Importante: Este precio es actualmente aleatorio. Una vez que tengas tu modelo de Machine Learning, deberás reemplazar la llamada a `get_random_price()` por la predicción de tu modelo.")

    st.subheader("Análisis de rentabilidad (TIR)")
    if precio_promedio_noche > 0:
        ingresos_brutos_diarios = precio_promedio_noche
        dias_ocupados_anuales = 365 * ocupacion_anual_porcentaje
        ingresos_brutos_anuales = ingresos_brutos_diarios * dias_ocupados_anuales
        costos_operacion_anuales = ingresos_brutos_anuales * costos_operacion_porcentaje
        flujo_caja_anual_neto = ingresos_brutos_anuales - costos_operacion_anuales

        inversion_total_inicial = inversion_inmueble + inversion_amueblar
        flujos_caja = [-inversion_total_inicial] + [flujo_caja_anual_neto]*horizonte_analisis_anos

        tir = calculate_irr(flujos_caja)

        if tir is not None:
            st.metric("Tasa Interna de Retorno (TIR)", f"{tir:.2%}")
            if tir > tasa_descuento_objetivo:
                st.success(f"💸 ¡Excelente! La TIR ({tir:.2%}) es mayor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). Este proyecto parece ser una buena inversión.")
                st.balloons()
            else:
                st.warning(f"⚠️ Atención: La TIR ({tir:.2%}) es menor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). Podría no ser tan atractiva.")
        else:
            st.error("No se pudo calcular la TIR. Verifica los flujos de caja.")
            st.info(f"Flujos de Caja: {flujos_caja}")
    else:
        st.warning("No se puede calcular la rentabilidad si el precio por noche es cero o negativo.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Desarrollado por Latam&Spain Soluciones Digitales.")
