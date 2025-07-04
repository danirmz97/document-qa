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
st.set_page_config(layout="centered", page_title="SmartRental") # Configuración de la página
st.markdown("""
    <style>
    /* --- COLOR PARA EL MULTISELECT (CIUDAD SELECCIONADA) --- */
    span.css-1n6fa23 {
        background-color: #4099c6 !important;
        color: white !important;
    }

    /* --- COLOR PARA EL NÚMERO DEL SLIDER --- */
    div[data-testid="stThumbValue"] {
        color: #4099c6 !important;
        font-weight: bold;
    }

    /* --- COLOR PARA LA BARRA DEL SLIDER --- */
    div[data-baseweb="slider"] > div > div {
        background-color: #4099c6 !important;
    }

    /* --- COLOR PARA EL CÍRCULO DEL SLIDER --- */
    div[data-testid="slider-thumb"] {
        background-color: #4099c6 !important;
    }
    </style>
""", unsafe_allow_html=True)

col_logo, col_title = st.columns([1, 5])  # Ajustamos el ancho de las columnas

with col_logo:
    st.image("Título-removebg-preview.png", width=80)  # Tamaño ideal del logo

with col_title:
    st.markdown("<h1 style='font-size:36px; margin: 0;'>SmartRental</h1>", unsafe_allow_html=True)  # Título proporcional

st.markdown("""
Esta herramienta permite evaluar la viabilidad de invertir en un inmueble para alquiler turístico a través de Airbnb.

Con base en los datos ingresados, se estima:

- El **precio promedio por noche**,
- La **Tasa Interna de Retorno (TIR)** esperada,
- Y una **recomendación final** sobre la conveniencia de la inversión.

Proporciona una visión inicial para apoyar la toma de decisiones.
""")
st.markdown("---")


# --- 4. Inputs del inmueble (usuario) ---
st.markdown("<h2 style='font-size:28px;'>1. Datos del Inmueble</h2>", unsafe_allow_html=True)


ciudad = st.multiselect(
    "Ubicación (ciudad):",
    options=CIUDADES_DISPONIBLES,
    default=["Barcelona"] if "Barcelona" in CIUDADES_DISPONIBLES else [],
    max_selections=1,
    placeholder="Escribe para buscar o selecciona una ciudad...",
    help="Seleccione la ciudad donde se encuentra el inmueble."
)

room_type = st.selectbox(
    "Tipo de alojamiento:",
    ["Piso entero", "Habitación privada"],
    help="Seleccione el tipo de alojamiento que desee."
)

numero_personas = st.slider(
    "Número de huéspedes:",
    min_value=1, max_value=20, value=4,
    help="Seleccione la capacidad máxima de huéspedes."
)

bathrooms = st.number_input(
    "Número de baños:",
    min_value=1.0,
    max_value=10.0,
    step=0.5,
    value=1.0,
    help="Seleccione la cantidad total de baños disponibles."
)

bedrooms = st.number_input(
    "Número de dormitorios:",
    min_value=1,
    max_value=10,
    value=2,
    help="Seleccione la cantidad total de dormitorios."
)

beds = st.number_input(
    "Número de camas:",
    min_value=1,
    max_value=20,
    value=3,
    help="Seleccione la cantidad total de camas disponibles."
)

min_nights = st.number_input(
    "Estancia mínima (noches):",
    min_value=1,
    max_value=365,
    value=2,
    help="Seleccione el número mínimo de noches para reservar."
)

max_nights = st.number_input(
    "Estancia máxima (noches):",
    min_value=min_nights,
    max_value=365,
    value=30,
    help="Seleccione el número máximo de noches permitidas por reserva."
)

# --- 5. Selección de amenidades ---
st.markdown("<h2 style='font-size:28px;'>2. Selección de amenidades</h2>", unsafe_allow_html=True)

# --- Diccionario: categorías y sus amenities (claves internas) ---
amenities_por_categoria = {
    "Tecnología y Entretenimiento": ["wifi", "tv", "sound_system", "streaming_services", "game_console"],
    "Seguridad": ["security_guard", "security_system", "window_guards", "lockbox", "smoke_alarm", "carbon_monoxide_alarm", "first_aid_kit", "fire_extinguisher", "lock_on_bedroom_door"],
    "Baño y Bienestar": ["spa_access", "bathtub", "body_soap", "shampoo", "conditioner", "shower_gel", "vegan_shampoo", "vegan_conditioner", "vegan_soap", "hair_dryer", "essentials"],
    "Lavandería y Limpieza": ["washer", "dryer", "iron", "housekeeping"],
    "Vistas y Espacios Exteriores": ["garden", "balcony", "waterfront", "shared_backyard", "mountain_view", "hammock"],
    "Accesibilidad y Movilidad": ["parking", "free_parking", "elevator", "luggage_dropoff", "long_term_stays", "private_entrance"],
    "Climatización y Confort": ["air_conditioning", "heating", "workspace", "hot_water_kettle", "pool", "hot_tub", "sauna"],
    "Cocina y Comida": ["kitchen", "coffee_maker", "microwave", "refrigerator", "dishwasher", "oven", "toaster", "blender", "waiststaff", "bar", "breakfast_bar", "bread_maker", "gas_stove", "electric_stove", "induction_stove", "chef_service", "bbq_grill"],
    "Deporte, Salud y Ocio": ["exercise_equipment", "ski_in_ski_out", "ski_in_out", "golf_course_view", "gym", "sports_court", "table_sports", "board_games", "bicycle"],
    "Familia y Bebé": ["children_books_toys", "baby_bath", "baby_monitor", "crib", "baby_care"]
}

# --- Traducciones de amenities al español ---
amenity_traducciones = {
    "wifi": "WiFi", "tv": "Televisión", "sound_system": "Sistema de sonido", "streaming_services": "Servicios de streaming",
    "game_console": "Consola de videojuegos", "security_guard": "Guardia de seguridad", "security_system": "Sistema de seguridad",
    "window_guards": "Rejas en ventanas", "lockbox": "Caja de seguridad", "smoke_alarm": "Detector de humo",
    "carbon_monoxide_alarm": "Detector de monóxido de carbono", "first_aid_kit": "Botiquín de primeros auxilios",
    "fire_extinguisher": "Extintor", "lock_on_bedroom_door": "Cerradura en dormitorio", "spa_access": "Acceso a spa",
    "bathtub": "Bañera", "body_soap": "Jabón corporal", "shampoo": "Champú", "conditioner": "Acondicionador",
    "shower_gel": "Gel de ducha", "vegan_shampoo": "Champú vegano", "vegan_conditioner": "Acondicionador vegano",
    "vegan_soap": "Jabón vegano", "hair_dryer": "Secador de pelo", "essentials": "Esenciales (toallas, sábanas)",
    "washer": "Lavadora", "dryer": "Secadora", "iron": "Plancha", "housekeeping": "Servicio de limpieza",
    "garden": "Jardín", "balcony": "Balcón", "waterfront": "Frente al mar", "shared_backyard": "Patio compartido",
    "mountain_view": "Vista a la montaña", "hammock": "Hamaca", "parking": "Estacionamiento",
    "free_parking": "Estacionamiento gratuito", "elevator": "Ascensor", "luggage_dropoff": "Depósito de equipaje",
    "long_term_stays": "Estancias largas", "private_entrance": "Entrada privada", "air_conditioning": "Aire acondicionado",
    "heating": "Calefacción", "workspace": "Zona de trabajo", "hot_water_kettle": "Hervidor de agua", "pool": "Piscina",
    "hot_tub": "Jacuzzi", "sauna": "Sauna", "kitchen": "Cocina", "coffee_maker": "Cafetera", "microwave": "Microondas",
    "refrigerator": "Refrigerador", "dishwasher": "Lavavajillas", "oven": "Horno", "toaster": "Tostadora", "blender": "Licuadora",
    "waiststaff": "Personal de cocina", "bar": "Bar", "breakfast_bar": "Desayunador", "bread_maker": "Panificadora",
    "gas_stove": "Cocina a gas", "electric_stove": "Cocina eléctrica", "induction_stove": "Cocina de inducción",
    "chef_service": "Servicio de chef", "bbq_grill": "Parrilla", "exercise_equipment": "Equipo de ejercicio",
    "ski_in_ski_out": "Acceso directo a pistas de esquí", "ski_in_out": "Acceso a esquí",
    "golf_course_view": "Vista al campo de golf", "gym": "Gimnasio", "sports_court": "Cancha deportiva",
    "table_sports": "Juegos de mesa", "board_games": "Juegos de tablero", "bicycle": "Bicicletas",
    "children_books_toys": "Juguetes y libros infantiles", "baby_bath": "Bañera para bebé",
    "baby_monitor": "Vigilabebés", "crib": "Cuna", "baby_care": "Cuidados para bebé"
}

# --- Selector tipo checkbox (como en la imagen que enviaste) ---
st.markdown("<h3 style='font-size:22px;'>Tipo de amenidades</h3>", unsafe_allow_html=True)
categorias_seleccionadas = []

for categoria in amenities_por_categoria.keys():
    if st.checkbox(categoria, key=f"cat_{categoria}"):
        categorias_seleccionadas.append(categoria)

# --- Mostrar multiselects según lo que marcó el usuario ---
amenities_seleccionadas = {}

for categoria in categorias_seleccionadas:
    opciones = amenities_por_categoria[categoria]
    seleccionadas = st.multiselect(
        f"Seleccione las amenidades en {categoria} que desee:",
        options=opciones,
        format_func=lambda x: amenity_traducciones.get(x, x),
        key=f"amenities_{categoria}"
    )
    amenities_seleccionadas[categoria] = seleccionadas

# --- 6. Costes de inversión (usuario) ---
st.markdown("<h2 style='font-size:28px;'>3. Costes de inversión</h2>", unsafe_allow_html=True)

inversion_inmueble = st.number_input(
    "Inversión inicial del inmueble:",
    min_value=10000.0, value=150000.0, step=1000.0, format="%.2f",
    help="Introduzca el coste aproximado del inmueble."
)

inversion_amueblar = st.number_input(
    "Inversión en amueblar y equipar:",
    min_value=0.0, value=20000.0, step=500.0, format="%.2f",
    help="Introduzca el coste aproximado de equipamiento del inmueble."
)

inversion_costes_admin = st.number_input(
    "Costes administrativos anuales:",
    min_value=0.0, value=5000.0, step=500.0, format="%.2f",
    help="Incluye gastos como notaría, impuestos, gestoría, etc."
)

st.markdown("---")


# --- 6. Botón para Calcular ---
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #4099c6;
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 0.5em;
        font-weight: bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #4099c6;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if st.button("Calcular precio y rentabilidad 🚀", type="primary"):
    st.markdown("<h2 style='font-size:28px;'>4. Resultados del Análisis</h2>", unsafe_allow_html=True)

    # --- Output de Precio (SIMULADO) ---
    precio_promedio_noche = get_random_price() # Llama a la función para obtener el precio aleatorio
    st.markdown(f"""
<h3 style='font-size:22px;'>
    Precio promedio por noche estimado: 
    <strong style='color:#386d79;'>{precio_promedio_noche:,.2f} €</strong>
</h3>
""", unsafe_allow_html=True)

    st.info("🚨 **Nota Importante:** Este precio es actualmente **aleatorio**. Una vez que tengas tu modelo de Machine Learning, deberás reemplazar la llamada a `get_random_price()` por la predicción de tu modelo.")
    st.markdown("---")

    # --- Cálculo de Rentabilidad (TIR) ---
    st.markdown("<h3 style='font-size:22px;'>Análisis de Rentabilidad (TIR)</h3>", unsafe_allow_html=True)

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
            # Seleccionar color en función de la TIR
            color_tir = "#2E8B57" if tir >= tasa_descuento_objetivo else "#D9534F"

            st.markdown(f"""
            <h3 style='font-size:22px;'>
                TIR estimada: 
                <strong style='color:{color_tir};'>{tir:.2%}</strong>
            </h3>
            """, unsafe_allow_html=True)

            if tir > tasa_descuento_objetivo:
                st.success(f"💸 *¡Excelente!* La TIR ({tir:.2%}) es mayor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). "
                           "Este proyecto parece ser una *buena inversión* bajo tus criterios de rentabilidad.")
                st.balloons()  # Pequeña celebración visual
            else:
                st.warning(f"⚠️ *Atención:* La TIR ({tir:.2%}) es menor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). "
                           "Considera revisar los inputs o si esta inversión cumple con tus expectativas de rentabilidad. Podría no ser tan atractiva.")
        else:
            st.error("No se pudo calcular la TIR con los flujos de caja proporcionados. Asegúrate de que haya una inversión inicial negativa seguida de flujos positivos.")
            st.info(f"Flujos de Caja generados: {flujos_caja}")  # Ayuda para depurar

    else:
        st.warning("No se puede calcular la rentabilidad si el precio por noche es cero o negativo.")

# --- 7. Pie de Página ---
st.markdown("---")

col_logo_footer, col_text_footer = st.columns([1, 8])

with col_logo_footer:
    st.image("Título-removebg-preview.png", width=40)

with col_text_footer:
    st.markdown("<p style='font-size:14px; margin-top: 12px;'>Desarrollado por Latam&Spain Digital Solutions</p>", unsafe_allow_html=True)

st.caption("Disclaimer: Esta herramienta proporciona estimaciones generales para una toma de decisión inicial.")
