import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import unicodedata

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

pilots = pd.read_csv("pilots.csv")
pilots.columns = pilots.columns.str.strip()


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

st.title("🏍️ Pilot del dia")

st.image(f"images/{pilot_dia['image']}", use_container_width=True)

if st.session_state.encertat:
    st.success("🏁 Ja has resolt el repte d’avui. Torna demà!")
    st.info("⏰ El proper pilot apareixerà demà a les 8:00")
    st.stop()

guess = st.text_input("Quin pilot és?")

if guess:
    if normalitza(guess) == normalitza(pilot_dia["name"]):
        st.session_state.encertat = True
        st.success("✅ Correcte! Has encertat el pilot del dia!")
        st.balloons()
        st.stop()
    else:
        st.error("❌ No és correcte, torna-ho a provar!")


