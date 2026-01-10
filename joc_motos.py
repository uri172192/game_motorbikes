import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import unicodedata
from pathlib import Path

# -------------------------
# Configuració base
# -------------------------
st.set_page_config(page_title="Pilot de Motos del Dia")

BASE_DIR = Path(__file__).parent

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
    st.error("Error: pilots.csv està buit o no s'ha trobat.")
    st.stop()

index = dia_del_joc().toordinal() % len(pilots)
pilot_dia = pilots.iloc[index]

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
st.title("🏍️ Repte Pilot del dia")

image_path = BASE_DIR / "Fotos" / pilot_dia["image"]

if image_path.exists():
    st.image(image_path, use_container_width=True)
else:
    st.error(f"❌ No s'ha trobat la imatge: {pilot_dia['image']}")
    st.write("Ruta intentada:", image_path)

guess = st.text_input("🔎 Quin pilot és?")
if guess:
    if normalitza(guess) == normalitza(pilot_dia["name"]):
        st.session_state.encertat = True
        st.success("✅ Correcte! Has encertat el pilot del dia!")
        st.balloons()
        st.stop()
    else:
        st.error("❌ No és correcte, torna-ho a provar!")

if st.button("👀 Mostrar la resposta"):
    st.session_state.mostrar_resposta = True

if st.session_state.mostrar_resposta:
    st.info(f"🧠 La resposta correcta és: **{pilot_dia['name']}**")
    st.session_state.mostrar_resposta = False
