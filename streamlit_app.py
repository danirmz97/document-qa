import streamlit as st

# --- 3. Título y Descripción de la Aplicación ---
st.set_page_config(layout="centered", page_title="SmartRental") # Configuración de la página

st.markdown("""
    <style>
    /* Cambiar los chips de multiselect (rojo por defecto) a azul */
    div[data-baseweb="tag"] {
        background-color: #4099c6 !important;
        color: white !important;
        border: none !important;
    }

    /* Cambiar el botón "x" de cada chip a blanco */
    div[data-baseweb="tag"] svg {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
import random # Para generar un precio aleatorio
import pickle
from scipy.optimize import newton # Para el cálculo de TIR

# app.py (en la parte superior de tu script, después de los imports)

CIUDADES_DISPONIBLES = [
    "Seattle",
    "Sicily", 
    "South Aegean",
    "Barwon South West Vic",
    "Madrid",
    "Pacific Grove",
    "Belize",
    "San Mateo County",
    "Northern Rivers",
    "Mid North Coast",
    "Columbus",
    "Quebec City",
    "Greater Manchester",
    "Sunshine Coast",
    "Salem Or",
    "Ghent",
    "Mornington Peninsula",
    "Barossa Valley",
    "New Brunswick",
    "Victoria",
    "Broward County",
    "Rhode Island",
    "Montreal",
    "Toronto",
    "Vancouver",
    "Ottawa",
    "Winnipeg",
    "Albany",
    "Asheville",
    "Austin",
    "Boston",
    "Bozeman",
    "Cambridge",
    "Chicago",
    "Clark County Nv",
    "Dallas",
    "Denver",
    "Fort Worth",
    "Hawaii",
    "Jersey City",
    "Los Angeles",
    "Nashville",
    "New Orleans",
    "New York City",
    "Newark",
    "Oakland",
    "Portland",
    "Vienna",
    "Antwerp",
    "Brussels",
    "Copenhagen",
    "Bordeaux",
    "Athens",
    "Crete",
    "Thessaloniki",
    "Bologna",
    "Florence",
    "Naples",
    "Venice",
    "Lisbon",
    "Stockholm",
    "Vaud",
    "Edinburgh",
    "Western Australia",
    "Singapore",
    "Twin Cities Msa",
    "Washington Dc",
    "Rome",
    "Rochester",
    "San Diego",
    "San Francisco",
    "Santa Clara County",
    "Santa Cruz County",
    "Lyon",
    "Paris",
    "Pays Basque",
    "Berlin",
    "Munich",
    "Dublin",
    "Bergamo",
    "Milan",
    "Puglia",
    "Trentino",
    "Riga",
    "Oslo",
    "Porto",
    "Barcelona",
    "Euskadi",
    "Girona",
    "Malaga",
    "Mallorca",
    "Menorca",
    "Sevilla",
    "Valencia",
    "Geneva",
    "Zurich",
    "Bristol",
    "London",
    "Cape Town",
    "Brisbane",
    "Melbourne",
    "Sydney",
    "Tasmania",
    "Hong Kong",
    "Tokyo",
    "Bangkok",
    "Buenos Aires",
    "Rio De Janeiro",
    "Santiago",
    "Mexico City",
    "Budapest"
]

city_mapping = {
    "seattle": 1,
    "sicily": 2,
    "south-aegean": 3,
    "barwon-south-west-vic": 4,
    "madrid": 5,
    "pacific-grove": 6,
    "belize": 7,
    "san-mateo-county": 8,
    "northern-rivers": 9,
    "mid-north-coast": 10,
    "columbus": 11,
    "quebec-city": 12,
    "greater-manchester": 13,
    "sunshine-coast": 14,
    "salem-or": 15,
    "ghent": 16,
    "mornington-peninsula": 17,
    "barossa-valley": 18,
    "new-brunswick": 19,
    "victoria": 20,
    "broward-county": 21,
    "rhode-island": 22,
    "montreal": 23,
    "toronto": 24,
    "vancouver": 25,
    "ottawa": 26,
    "winnipeg": 27,
    "albany": 28,
    "asheville": 29,
    "austin": 30,
    "boston": 31,
    "bozeman": 32,
    "cambridge": 33,
    "chicago": 34,
    "clark-county-nv": 35,
    "dallas": 36,
    "denver": 37,
    "fort-worth": 38,
    "hawaii": 39,
    "jersey-city": 40,
    "los-angeles": 41,
    "nashville": 42,
    "new-orleans": 43,
    "new-york-city": 44,
    "newark": 45,
    "oakland": 46,
    "portland": 47,
    "vienna": 48,
    "antwerp": 49,
    "brussels": 50,
    "copenhagen": 51,
    "bordeaux": 52,
    "athens": 53,
    "crete": 54,
    "thessaloniki": 55,
    "bologna": 56,
    "florence": 57,
    "naples": 58,
    "venice": 59,
    "lisbon": 60,
    "stockholm": 61,
    "vaud": 62,
    "edinburgh": 63,
    "western-australia": 64,
    "singapore": 65,
    "twin-cities-msa": 66,
    "washington-dc": 67,
    "rome": 68,
    "rochester": 69,
    "san-diego": 70,
    "san-francisco": 71,
    "santa-clara-county": 72,
    "santa-cruz-county": 73,
    "lyon": 74,
    "paris": 75,
    "pays-basque": 76,
    "berlin": 77,
    "munich": 78,
    "dublin": 79,
    "bergamo": 80,
    "milan": 81,
    "puglia": 82,
    "trentino": 83,
    "riga": 84,
    "oslo": 85,
    "porto": 86,
    "barcelona": 87,
    "euskadi": 88,
    "girona": 89,
    "malaga": 90,
    "mallorca": 91,
    "menorca": 92,
    "sevilla": 93,
    "valencia": 94,
    "geneva": 95,
    "zurich": 96,
    "bristol": 97,
    "london": 98,
    "cape-town": 99,
    "brisbane": 100,
    "melbourne": 101,
    "sydney": 102,
    "tasmania": 103,
    "hong-kong": 104,
    "tokyo": 105,
    "bangkok": 106,
    "buenos-aires": 107,
    "rio-de-janeiro": 108,
    "santiago": 109,
    "mexico-city": 110,
    "budapest": 111
}

import re

def normalize_city_name(city_name):
    """
    Normaliza el nombre de la ciudad para hacer coincidencias.
    Convierte a minúsculas, reemplaza espacios por guiones, y elimina caracteres especiales.
    """
    if not city_name:
        return ""
    
    # Convertir a minúsculas
    normalized = city_name.lower()
    
    # Reemplazar espacios y caracteres especiales por guiones
    normalized = re.sub(r'[\s\-_]+', '-', normalized)
    
    # Eliminar caracteres especiales excepto guiones
    normalized = re.sub(r'[^\w\-]', '', normalized)
    
    # Eliminar guiones múltiples
    normalized = re.sub(r'-+', '-', normalized)
    
    # Eliminar guiones al inicio y final
    normalized = normalized.strip('-')
    
    return normalized


costos_operacion_porcentaje = .5


tasa_descuento_objetivo = .10

horizonte_analisis_anos = 10


@st.cache_resource
def load_model():
    """
    Carga el modelo de ML una sola vez y lo mantiene en caché.
    Se ejecuta solo la primera vez o cuando cambia el archivo del modelo.
    """
    filename = "price_model.pkl"
    model_path = f"./{filename}"
    
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        print(f"✅ Modelo cargado: {model_path}")
        return model
    except FileNotFoundError:
        st.error(f"❌ No se encontró el archivo del modelo: {model_path}")
        return None
    except Exception as e:
        st.error(f"❌ Error al cargar el modelo: {e}")
        return None


def get_price(features_dict):
    features_df = pd.DataFrame([features_dict])
    model = load_model()
    result = model.predict(features_df)

    return result[0]

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

# CSS para reducir espacios
st.markdown("""
    <style>
    /* Reducir espacios en el mapa */
    .stApp > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    
    /* Reducir margen del mapa */
    iframe[title="streamlit_folium.st_folium"] {
        margin-bottom: 0 !important;
    }
    
    /* Reducir espacios entre elementos */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h3 style='font-size:22px;'>📍 Ubicación del inmueble</h3>", unsafe_allow_html=True)

# Inicializar coordenadas en session_state si no existen
if 'latitude' not in st.session_state:
    st.session_state.latitude = 41.3851  # Barcelona por defecto
if 'longitude' not in st.session_state:
    st.session_state.longitude = 2.1734

# Opción de selección de ubicación
ubicacion_metodo = st.radio(
    "¿Cómo prefieres indicar la ubicación?",
    ["🗺️ Seleccionar en el mapa", "📝 Introducir coordenadas manualmente"],
    help="Elige la forma más cómoda para ti de indicar la ubicación"
)

if ubicacion_metodo == "🗺️ Seleccionar en el mapa":
    st.info("💡 **Tip:** Haz clic en el mapa para seleccionar la ubicación exacta de tu propiedad")
    
    # Crear mapa con folium
    m = folium.Map(
        location=[st.session_state.latitude, st.session_state.longitude],
        zoom_start=12,
        width="100%",
        height=400
    )
    
    # Agregar marcador en la posición actual
    folium.Marker(
        [st.session_state.latitude, st.session_state.longitude],
        popup="📍 Tu propiedad",
        tooltip="Ubicación seleccionada",
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)
    
    # Mostrar mapa y capturar clics
    map_data = st_folium(
        m,
        key="location_map",
        width=700,
        height=400
    )
    
    # Actualizar coordenadas si se hizo clic en el mapa
    if map_data['last_clicked'] is not None:
        st.session_state.latitude = map_data['last_clicked']['lat']
        st.session_state.longitude = map_data['last_clicked']['lng']
        st.rerun()  # Recargar para actualizar el mapa
    
    # Campos de coordenadas que se actualizan con el mapa
    col1, col2 = st.columns(2)
    
    with col1:
        new_latitude = st.number_input(
            "📍 Latitud",
            value=st.session_state.latitude,
            format="%.6f",
            help="Coordenada de latitud (Norte-Sur). Cambia automáticamente al hacer clic en el mapa.",
            key="lat_input"
        )
    
    with col2:
        new_longitude = st.number_input(
            "📍 Longitud", 
            value=st.session_state.longitude,
            format="%.6f",
            help="Coordenada de longitud (Este-Oeste). Cambia automáticamente al hacer clic en el mapa.",
            key="lng_input"
        )
    
    # Actualizar session_state si se cambiaron manualmente las coordenadas
    if new_latitude != st.session_state.latitude or new_longitude != st.session_state.longitude:
        st.session_state.latitude = new_latitude
        st.session_state.longitude = new_longitude
        st.rerun()  # Recargar para actualizar el mapa

else:
    # Opción manual con mejor UX
    st.info("💡 **Tip:** Puedes obtener las coordenadas desde Google Maps: clic derecho → 'Ver coordenadas'")
    
    col1, col2 = st.columns(2)
    
    with col1:
        latitude = st.number_input(
            "📍 Latitud",
            min_value=-90.0,
            max_value=90.0,
            value=st.session_state.latitude,
            format="%.6f",
            help="Ejemplo: 41.385064 (para Barcelona). Rango válido: -90 a 90"
        )
    
    with col2:
        longitude = st.number_input(
            "📍 Longitud",
            min_value=-180.0, 
            max_value=180.0,
            value=st.session_state.longitude,
            format="%.6f",
            help="Ejemplo: 2.173404 (para Barcelona). Rango válido: -180 a 180"
        )
    
    # Actualizar session_state
    st.session_state.latitude = latitude
    st.session_state.longitude = longitude
    
    # Mostrar ubicación seleccionada en mapa
    if latitude and longitude:
        preview_map = folium.Map(
            location=[latitude, longitude],
            zoom_start=15,
            width=700,
            height=300
        )
        
        folium.Marker(
            [latitude, longitude],
            popup="📍 Ubicación seleccionada",
            icon=folium.Icon(color='blue', icon='home')
        ).add_to(preview_map)
        
        st.caption("📍 Vista previa de la ubicación:")
        st_folium(preview_map, width=700, height=300, key="preview_map")

# Mostrar coordenadas finales
st.success(f"📍 **Coordenadas seleccionadas:** {st.session_state.latitude:.6f}, {st.session_state.longitude:.6f}")

# Variables que puedes usar en el resto de tu código
latitude = st.session_state.latitude
longitude = st.session_state.longitude

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

print(amenities_seleccionadas)

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

costos_operacion_anuales = st.number_input(
    "Costes administrativos anuales:",
    min_value=0.0, value=5000.0, step=500.0, format="%.2f",
    help="Incluye gastos como notaría, impuestos, gestoría, etc."
)

st.markdown("<h2 style='font-size:28px;'>4. Ocupación anual</h2>", unsafe_allow_html=True)

ocupacion_anual_porcentaje = st.number_input(
    "Porcentaje de ocupación anual:",
    min_value=0.0, max_value=1.0, value=0.7, step=0.1, format="%.2f",
    help="Especifica el porcentaje de ocupación anual, este valor lo puedes consultar en el dashboard para la ciudad escogida"
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
    city = normalize_city_name(ciudad[0])
    try:
        city_label = city_mapping[city]
    except:
        st.error("🚨🚨🚨🚨Ciudad no encontrada🚨🚨🚨🚨")
        pass

    amenitie_total = sum(len(amenities_seleccionadas.get(categoria, [])) for categoria in [
        "Accesibilidad y Movilidad", "Baño y Bienestar", "Climatización y Confort", 
        "Cocina y Comida", "Deporte, Salud y Ocio", "Familia y Bebé", 
        "Lavandería y Limpieza", "Seguridad", "Tecnología y Entretenimiento", 
        "Vistas y Espacios Exteriores"
    ])

    data = {
        "latitude": latitude,
        "longitude": longitude,
        "accommodates": numero_personas,
        "bathrooms": bathrooms,
        "bedrooms": bedrooms,
        "beds": beds,
        "minimum_nights": min_nights,
        "maximum_nights": max_nights,
        "accesibilidad_y_movilidad_count": len(amenities_seleccionadas.get("Accesibilidad y Movilidad", [])),
        "baño_y_bienestar_count": len(amenities_seleccionadas.get("Baño y Bienestar", [])),
        "climatización_y_confort_count": len(amenities_seleccionadas.get("Climatización y Confort", [])),
        "cocina_y_comida_count": len(amenities_seleccionadas.get("Cocina y Comida", [])),
        "deporte_salud_y_ocio_count": len(amenities_seleccionadas.get("Deporte, Salud y Ocio", [])),
        "familia_y_bebé_count": len(amenities_seleccionadas.get("Familia y Bebé", [])),
        "lavandería_y_limpieza_count": len(amenities_seleccionadas.get("Lavandería y Limpieza", [])),
        "seguridad_count": len(amenities_seleccionadas.get("Seguridad", [])),
        "tecnología_y_entretenimiento_count": len(amenities_seleccionadas.get("Tecnología y Entretenimiento", [])),
        "vistas_y_espacios_exteriores_count": len(amenities_seleccionadas.get("Vistas y Espacios Exteriores", [])),
        "total_amenities_count": amenitie_total,
        "city_label": city_label,
        "room_type_entire home/apt": 1 if room_type == "Piso entero" else 0,
        "room_type_hotel room": 0,
        "room_type_private room": 1 if room_type == "Habitación privada" else 0,
        "room_type_shared room": 0
    }

    precio_promedio_noche = get_price(data)
    st.markdown(f"""
<h3 style='font-size:22px;'>
    Precio promedio por noche estimado: 
    <strong style='color:#386d79;'>{precio_promedio_noche:,.2f} $</strong>
</h3>
""", unsafe_allow_html=True)

    # --- Cálculo de Rentabilidad (TIR) ---

    if precio_promedio_noche > 0:
        ingresos_brutos_diarios = precio_promedio_noche
        dias_ocupados_anuales = 365 * ocupacion_anual_porcentaje
        ingresos_brutos_anuales = ingresos_brutos_diarios * dias_ocupados_anuales

        flujo_caja_anual_neto = ingresos_brutos_anuales - costos_operacion_anuales

        # Crear flujos de caja para la TIR
        # El primer flujo es la inversión inicial (negativa)
        inversion_total_inicial = inversion_inmueble + inversion_amueblar
        flujos_caja = [-inversion_total_inicial]

        # Luego, los flujos de caja anuales netos para el horizonte de análisis
        for _ in range(horizonte_analisis_anos - 1):
            flujos_caja.append(flujo_caja_anual_neto)

        flujos_caja.append(inversion_inmueble)

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
                st.markdown("<h1 style='text-align: center;'>💰💰💸 ¡Rentabilidad! 💸💰💰</h1>", unsafe_allow_html=True)
                st.success(f"💸 *¡Excelente!* La TIR ({tir:.2%}) es mayor que tu tasa de descuento objetivo ({tasa_descuento_objetivo:.2%}). "
               "Este proyecto parece ser una *buena inversión* bajo tus criterios de rentabilidad.")

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
