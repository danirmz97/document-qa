import streamlit as st
import pandas as pd
import numpy as np
import random # Para generar un precio aleatorio
from scipy.optimize import newton # Para el cálculo de TIR
# app.py (en la parte superior de tu script, después de los imports)

CIUDADES_DISPONIBLES = [
    "Albany", "Albacete", "Alicante", "Almería", "Alcalá de Henares", "Alcoy", "Algeciras", "Amsterdam", "Amberes",
    "Antequera", "Arrecife", "Arganda del Rey", "Asheville", "Atenas", "Austin", "Ávila", "Badalona", "Bangkok",
    "Barcelona", "Barossa", "Barwon", "Beijin", "Belice", "Benidorm", "Bergamo", "Berlín", "Bilbao", "Bolonia",
    "Boston", "Bozeman", "Bristol", "Brisbane", "Broward County", "Bruselas", "Buenos Aires", "Burgos", "Burdeos",
    "Cáceres", "Cádiz", "Cambridge", "Cape Town", "Cartagena", "Castelló de la Plana", "Ceuta", "Chicago",
    "Chiclana de la Frontera", "Ciudad Real", "Clark County", "Collado Villalba", "Colón", "Copenhague", "Córdoba",
    "Creta", "Cuenca", "Dallas", "Denver", "Donostia-San Sebastián", "Dos Hermanas", "Dublín", "Edimburgo", "Egeo",
    "Elche", "Eskadi", "Estepona", "Ferrol", "Florencia", "Fort Worth", "Fuenlabrada", "Fuengirola", "Gante",
    "Geneva", "Getafe", "Getxo", "Gijón", "Girona", "Granada", "Guadalajara", "Hawai", "Hong Kong", "Huesca",
    "Huelva", "Istanbul", "Jaén", "Jersey City", "Jerez de la Frontera", "La Haya", "L'Hospitalet de Llobregat",
    "Las Palmas de Gran Canaria", "Leganés", "León", "Lisboa", "Logroño", "Lorca", "Los Angeles", "Lugo", "Londres",
    "Lyon", "Madrid", "Majadahonda", "Málaga", "Mallorca", "Manchester", "Marbella", "Mataró", "Melbourne",
    "Menorca", "Mexico City", "Milán", "Móstoles", "Montreal", "Mornington", "Munich", "Murcia", "Nápoles",
    "Nashville", "New Brunswick", "New Orleans", "New York", "Newark", "New Wales", "Oakland", "Orihuela", "Oslo",
    "Ottawa", "Ourense", "Oviedo", "Pacific Northwest Forests", "Pais Vasco", "Palencia", "Palma de Mallorca",
    "Pamplona", "París", "Parla", "Pontevedra", "Porto", "Portland", "Pozuelo de Alarcón", "Praga", "Puglia",
    "Puerto de Santa María", "Quebec", "Queensland", "Reus", "Rhode Island", "Riga", "Río de Janeiro",
    "Rivas-Vaciamadrid", "Rochester", "Roma", "Roquetas de Mar", "Róterdam", "Sabadell", "Sagunto", "Salem",
    "Salamanca", "San Diego", "San Fernando", "San Francisco", "San Mateo", "San Sebastián de los Reyes", "Santa Clara",
    "Santa Coloma de Gramenet", "Santa Cruz", "Santa Cruz de Tenerife", "Santiago", "Seattle", "Segovia", "Sevilla",
    "Shanghái", "Sicilia", "Singapur", "Soria", "Estocolmo", "Sídney", "Taipei", "Tarragona", "Tasmania", "Telde",
    "Terrassa", "The Hague", "Tokio", "Toledo", "Toronto", "Torrejón de Ardoz", "Torrelavega", "Trentino",
    "Twin Cities", "Valencia", "Valdemoro", "Valladolid", "Vancouver", "Vaudvaud", "Venecia", "Viena", "Vigo",
    "Villareal", "Vitoria-Gasteiz", "Washington", "West Australia", "Winnipeg", "Zamora", "Zaragoza", "Zúrich"
]

costos_operacion_porcentaje = .5

ocupacion_anual_porcentaje = .70

tasa_descuento_objetivo = .10

horizonte_analisis_anos = 10


# app.py (en la parte superior de tu script, después de los imports)


# --- 1. Simulación de Precio (PARA REEMPLAZAR DESPUÉS CON TU MODELO ML) ---
def get_random_price(min_price=50, max_price=300):
    """
    Genera un precio por noche aleatorio.
    Esto debe ser reemplazado por la predicción de tu modelo de Machine Learning.
    """
    return random.uniform(min_price, max_price)

# --- 2. Funciones de Cálculo de TIR (Tasa Interna de Retorno) ---

def npv_function(tir_guess, flujos):
    """
    Función que representa el VAN (Valor Actual Neto) para el cálculo de TIR.
    tir_guess: Es la tasa que estamos probando.
    flujos: Una lista o array de los flujos de caja del proyecto.
    """
    npv = 0
    for i, flujo in enumerate(flujos):
        npv += flujo / (1 + tir_guess)**i
    return npv

def calculate_irr(cash_flows):
    """
    Función para calcular la TIR.
    Utiliza el método de Newton para encontrar la raíz de la función VAN.
    """
    try:
        # Intentamos un valor inicial para la TIR. Si hay un flujo negativo inicial,
        # y luego positivos, la TIR debería ser computable.
        irr = newton(lambda r: npv_function(r, cash_flows), 0.10)
        return irr
    except RuntimeError:
        # En caso de que el método de Newton no converja
        st.warning("No se pudo encontrar una TIR. Esto puede ocurrir si los flujos de caja son inconsistentes (ej. todos positivos o todos negativos después de la inversión).")
        return None
    except ZeroDivisionError:
        # En caso de flujos de caja inconsistentes
        st.warning("Error matemático al calcular la TIR. Verifique los flujos de caja.")
        return None
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al calcular la TIR: {e}")
        return None


# --- 3. Título y Descripción de la Aplicación ---
st.set_page_config(layout="centered", page_title="Calculadora Airbnb") # Configuración de la página

col_logo, col_title = st.columns([1, 4]) # Una columna pequeña para el logo, una grande para el título

with col_logo:
    st.image("Logo.jpeg", width=100) # Ajusta el ancho según tu logo

with col_title:
    st.title("Calculadora de Rentabilidad")

st.markdown("""
Analiza la viabilidad de comprar un inmueble para renta en Airbnb.
Obtendrás un **precio promedio por noche**
y la **Tasa Interna de Retorno (TIR)** estimada. 
Finalmente la **Alerta de recomendación** para la compra o no del inmueble.
""")
st.markdown("---")

# --- 4. Inputs del inmueble (usuario) ---
st.header("1. Datos del Inmueble")

col1, col2 = st.columns(2)

with col1:
    ciudad = st.multiselect(
        "Ubicación (ciudad):",
        options=CIUDADES_DISPONIBLES,
        default=["Barcelona"] if "Barcelona" in CIUDADES_DISPONIBLES else [],
        max_selections=1,
         placeholder="Escribe para buscar o selecciona una ciudad...",
        help="Seleccione la ciudad donde se encuentra el inmueble."
    )
    numero_personas = st.slider(
        "Número de personas que puede alojar:",
        min_value=1, max_value=20, value=4, help="Capacidad máxima de huéspedes."
    )
    tamano_m2 = st.number_input(
        "Tamaño del inmueble (m²):",
        min_value=10, max_value=500, value=70, step=5, help="Metros cuadrados del inmueble."
    )

with col2:
    amenities_count = st.slider(
        "Número de comodidades/amenities (ej. piscina, gimnasio, wifi, AC, parking):",
        min_value=0, max_value=15, value=5, help="Cantidad de servicios adicionales que ofrece el inmueble."
    )



st.markdown("---")
# --- 6. Costes de inversión (usuario) ---
st.header("2. Costes de inversión")

inversion_inmueble = st.number_input(
    "Inversión inicial en el inmueble (€):",
    min_value=10000.0, value=150000.0, step=1000.0, format="%.2f", help="Costo de compra del inmueble."
)
inversion_amueblar = st.number_input(
    "Inversión en amueblar y equipar (€):",
    min_value=0.0, value=20000.0, step=500.0, format="%.2f", help="Costo de mobiliario y equipamiento."
)

st.markdown("---")

# --- 6. Botón para Calcular ---
if st.button("🚀 Calcular Precio y Rentabilidad", type="primary"):
    st.header("3. Resultados del Análisis")

    # --- Output de Precio (SIMULADO) ---
    precio_promedio_noche = get_random_price() # Llama a la función para obtener el precio aleatorio
    st.subheader(f"Precio Promedio por Noche Estimado: **€{precio_promedio_noche:,.2f}**")
    st.info("🚨 **Nota Importante:** Este precio es actualmente **aleatorio**. Una vez que tengas tu modelo de Machine Learning, deberás reemplazar la llamada a `get_random_price()` por la predicción de tu modelo.")
    st.markdown("---")

    # --- Cálculo de Rentabilidad (TIR) ---
    st.subheader("Análisis de Rentabilidad (TIR)")

    if precio_promedio_noche > 0:
        ingresos_brutos_diarios = precio_promedio_noche
        dias_ocupados_anuales = 365 * ocupacion_anual_porcentaje
        ingresos_brutos_anuales = ingresos_brutos_diarios * dias_ocupados_anuales

        costos_operacion_anuales = ingresos_brutos_anuales * costos_operacion_porcentaje

        flujo_caja_anual_neto = ingresos_brutos_anuales - costos_operacion_anuales

        # Crear flujos de caja para la TIR
        # El primer flujo es la inversión inicial (negativa)
        inversion_total_inicial = inversion_inmueble + inversion_amueblar
        flujos_caja = [-inversion_total_inicial]

        # Luego, los flujos de caja anuales netos para el horizonte de análisis
        for _ in range(horizonte_analisis_anos):
            flujos_caja.append(flujo_caja_anual_neto)

        # Opcional: Valor de rescate/venta del inmueble al final del período
        # Para un análisis más completo, se podría añadir un valor de venta estimado
        # del inmueble al final del horizonte. Por ahora, lo omitimos para simplicidad.
        # Por ejemplo: flujos_caja[-1] += valor_venta_final_estimado

        tir = calculate_irr(flujos_caja)

        if tir is not None:
            st.metric(label="Tasa Interna de Retorno (TIR)", value=f"{tir:.2%}")

            if tir > tasa_descuento_objetivo:
                st.success(f"💸 **¡Excelente!** La TIR ({tir:.2%}) es mayor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). "
                           "Este proyecto parece ser una **buena inversión** bajo tus criterios de rentabilidad.")
                st.balloons() # Pequeña celebración visual
            else:
                st.warning(f"⚠️ **Atención:** La TIR ({tir:.2%}) es menor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). "
                           "Considera revisar los inputs o si esta inversión cumple con tus expectativas de rentabilidad. Podría no ser tan atractiva.")
        else:
            st.error("No se pudo calcular la TIR con los flujos de caja proporcionados. Asegúrate de que haya una inversión inicial negativa seguida de flujos positivos.")
            st.info(f"Flujos de Caja generados: {flujos_caja}") # Ayuda para depurar
    else:
        st.warning("No se puede calcular la rentabilidad si el precio por noche es cero o negativo.")

# --- 7. Pie de Página ---
st.markdown("---")
st.caption("Desarrollado con ❤️ por Latam&Spain")
st.caption("Disclaimer: Esta herramienta proporciona estimaciones generales para una toma de decisión inicial.")

