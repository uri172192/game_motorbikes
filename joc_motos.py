import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import unicodedata
from pathlib import Path
import random
import hashlib

# -------------------------
# Configuració base
# -------------------------
st.set_page_config(page_title="Pilot de Motos del Dia")

BASE_DIR = Path(__file__).parent

# -------------------------
# Traducció Diccionari
# -------------------------
# Define translations for each language. Keys match UI elements.
# Add more languages by adding new top-level keys (e.g., 'es' for Spanish).
translations = {
    'ca': {  # Catalan (original)
        'page_title': "Pilot de Motos del Dia",
        'title': "🏍️ Repte Pilot del dia",
        'language_label': "🌐​Idioma",
        'language_options': {"Català": "ca", "English": "en", "Español":"es"},
        'error_empty_csv': "Error: pilots.csv està buit o no s'ha trobat.",
        'error_image_not_found': "❌ No s'ha trobat la imatge: {image}",
        'image_path_attempted': "Ruta intentada:",
        'guess_placeholder': "🔎 Quin pilot és?",
        'success_message': "✅ Correcte! Has encertat el pilot del dia!",
        'error_wrong_guess': "❌ No és correcte, torna-ho a provar!",
        'show_answer_button': "👀 Mostrar la resposta",
        'answer_reveal': "🧠 La resposta correcta és: **{name}**",
    },
    'en': {  # English
        'page_title': "Daily Motorcycle Pilot",
        'title': "🏍️ Daily Rider Challenge",
        'language_label': "🌐​Language",
        'language_options': {"Català": "ca", "English": "en", "Español":"es"},
        'error_empty_csv': "Error: pilots.csv is empty or not found.",
        'error_image_not_found': "❌ Image not found: {image}",
        'image_path_attempted': "Attempted path:",
        'guess_placeholder': "🔎 Which rider is it?",
        'success_message': "✅ Correct! You've guessed today's pilot!",
        'error_wrong_guess': "❌ Incorrect, try again!",
        'show_answer_button': "👀 Show the answer",
        'answer_reveal': "🧠 The correct answer is: **{name}**",
    },
    'es': {  # Español
        'page_title': "Piloto de Motos del Día",
        'title': "🏍️ Reto Piloto del día",
        'language_label': "🌐​Idioma",
        'language_options': {"Català": "ca", "English": "en","Español":"es"},
        'error_empty_csv': "Error:  pilots.csv está vacio o no se ha encontrado.",
        'error_image_not_found': "❌ Imagen no encontrada: {image}",
        'image_path_attempted': "Ruta intentada:",
        'guess_placeholder': "🔎 ¿Qué piloto es?",
        'success_message': "✅ ¡Correcto! ¡Has acertado el piloto del día!",
        'error_wrong_guess': "❌ ¡Incorrecto! ¡Prueba de nuevo!",
        'show_answer_button': "👀 Mostrar la respuesta",
        'answer_reveal': "🧠 La respuesta correcta es: **{name}**",
    }
}

# -------------------------
# Selecció Idioma
# -------------------------
# Initialize language in session state if not set (default to Catalan).
if "lang" not in st.session_state:
    st.session_state.lang = "ca"

# Language selector at the top (before other UI).
lang_display = st.selectbox(
    translations[st.session_state.lang]['language_label'],
    options=list(translations[st.session_state.lang]['language_options'].keys()),
    index=0 if st.session_state.lang == "ca" else 1,  # Default to Catalan
    key="lang_selector"
)
# Update session state based on selection.
st.session_state.lang = translations[st.session_state.lang]['language_options'][lang_display]

# Update page title dynamically (optional, as it's set once at the top).
#st.set_page_config(page_title=translations[st.session_state.lang]['page_title'])

# -------------------------
# Funcions
# -------------------------
from zoneinfo import ZoneInfo

def dia_del_joc():
    ara = datetime.now(ZoneInfo("Europe/Madrid"))
    if ara.hour < 8:
        ara -= timedelta(days=1)
    return ara.date()

def normalitza(text):
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

# -------------------------
# Carregar dades
# -------------------------
pilots = pd.read_csv(BASE_DIR / "pilots.csv", sep=";")

if len(pilots) == 0:
    st.error(translations[st.session_state.lang]['error_empty_csv'])
    st.stop()

if "ordre_random" not in st.session_state:
    st.session_state.ordre_random = pilots.sample(frac=1).reset_index(drop=True)

if "index_random" not in st.session_state:
    st.session_state.index_random = 0

def obtenir_pilot_del_dia(pilots):
    avui = dia_del_joc()

    n = len(pilots)

    data_inici = datetime(2025, 12, 24).date()
    dies_passats = (avui - data_inici).days

    cicle = dies_passats // n
    posicio = dies_passats % n

    seed = int(hashlib.sha256(f"pilot-{cicle}".encode()).hexdigest(), 16)

    rng = random.Random(seed)

    ids = pilots["id"].tolist()
    rng.shuffle(ids)

    id_pilot = ids[posicio]

    return pilots[pilots["id"] == id_pilot].iloc[0]
pilot_dia = obtenir_pilot_del_dia(pilots)

def obtenir_pilot_random():

    if st.session_state.index_random >= len(st.session_state.ordre_random):
        st.session_state.ordre_random = pilots.sample(frac=1).reset_index(drop=True)
        st.session_state.index_random = 0

    pilot = st.session_state.ordre_random.iloc[st.session_state.index_random]
    st.session_state.index_random += 1

    return pilot

# -------------------------
# Estat del joc
# -------------------------
if "encertat" not in st.session_state:
    st.session_state.encertat = False

if "mostrar_resposta" not in st.session_state:
    st.session_state.mostrar_resposta = False

# -------------------------
# UI
# -------------------------
st.title(translations[st.session_state.lang]['title'])

image_path = BASE_DIR / "Fotos" / pilot_dia["image"]
#print(f"Camí de la imatge: {image_path}")  # Afegeix això per depurar

if image_path.exists():
    st.image(image_path, use_container_width=True)
else:
    st.error(translations[st.session_state.lang]['error_image_not_found'].format(image=pilot_dia['image']))
    st.write(translations[st.session_state.lang]['image_path_attempted'], image_path)

guess = st.text_input(translations[st.session_state.lang]['guess_placeholder'])
if guess:
    if normalitza(guess) == normalitza(pilot_dia["name"]):
        st.session_state.encertat = True
        st.success(translations[st.session_state.lang]['success_message'])
        st.balloons()
        st.stop()
    else:
        st.error(translations[st.session_state.lang]['error_wrong_guess'])

if st.button(translations[st.session_state.lang]['show_answer_button']):
    st.session_state.mostrar_resposta = True

if st.session_state.mostrar_resposta:
    st.info(translations[st.session_state.lang]['answer_reveal'].format(name=pilot_dia['name']))
    st.session_state.mostrar_resposta = False

st.divider()

if st.button("🎲 Nou pilot"):

    st.session_state.pilot_random = obtenir_pilot_random()


if "pilot_random" in st.session_state:

    pilot = st.session_state.pilot_random

    st.subheader("Mode pràctica")

    image_path = BASE_DIR / "Fotos" / pilot["image"]

    st.image(image_path, use_container_width=True)

    resposta = st.text_input(
        "Qui és aquest pilot?",
        key="guess_random"
    )

    if resposta:

        if normalitza(resposta) == normalitza(pilot["name"]):
            st.success("✅ Correcte!")
        else:
            st.error("❌ Incorrecte")

    if st.button("👀 Mostrar resposta", key="mostrar_random"):
        st.info(pilot["name"])





