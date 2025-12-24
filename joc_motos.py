import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import unicodedata
import os

BASE_DIR = os.getcwd()  # Directori base per Streamlit

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
pilots = pd.read_csv("pilots.csv", sep=";")
#st.write("Columnes del CSV:", pilots.columns)
#st.write("Primeres files:", pilots.head())

index = dia_del_joc().toordinal() % len(pilots)
pilot_dia = pilots.iloc[index]

# -------------------------
# Estat del joc
# -------------------------
if "encertat" not in st.session_state:
    st.session_state.encertat = False

# -------------------------
# UI
# -------------------------
if len(pilots) == 0:
    st.error("Error: pilots.csv està buit o no s'ha trobat.")
else:
    st.title("🏍️ Pilot del dia")
    st.image(
        os.path.join(BASE_DIR, "Fotos", pilot_dia["image"]),
        use_container_width=True
    )

    guess = st.text_input("Quin pilot és?")
    if guess:
        if normalitza(guess) == normalitza(pilot_dia["name"]):
            st.session_state.encertat = True
            st.success("✅ Correcte! Has encertat el pilot del dia!")
            st.balloons()
            st.stop()
        else:
            st.error("❌ No és correcte, torna-ho a provar!")

