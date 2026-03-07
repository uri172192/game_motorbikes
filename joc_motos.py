import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import unicodedata
from pathlib import Path
import random

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
        'language_options': {"Català": "ca", "English": "en"},
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
        'language_options': {"Català": "ca", "English": "en"},
        'error_empty_csv': "Error: pilots.csv is empty or not found.",
        'error_image_not_found': "❌ Image not found: {image}",
        'image_path_attempted': "Attempted path:",
        'guess_placeholder': "🔎 Which rider is it?",
        'success_message': "✅ Correct! You've guessed today's pilot!",
        'error_wrong_guess': "❌ Incorrect, try again!",
        'show_answer_button': "👀 Show the answer",
        'answer_reveal': "🧠 The correct answer is: **{name}**",
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
def dia_del_joc():
    ara = datetime.now()
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

def obtenir_pilot_del_dia(pilots, dies_bloqueig=15):
    avui = dia_del_joc()
    seed_avui = avui.toordinal()

    # calcular els últims pilots dels darrers dies
    ultims = set()

    for i in range(1, dies_bloqueig + 1):
        seed_passat = (avui - timedelta(days=i)).toordinal()
        random.seed(seed_passat)
        idx = random.randint(0, len(pilots) - 1)
        ultims.add(idx)

    # generar pilot d'avui evitant repeticions
    random.seed(seed_avui)

    while True:
        idx = random.randint(0, len(pilots) - 1)
        if idx not in ultims:
            return pilots.iloc[idx]

pilot_dia = obtenir_pilot_del_dia(pilots)

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








