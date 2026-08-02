import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
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
        'tab_daily': "🏍️ Pilot del dia",
        'tab_practice': "🎲 Mode pràctica",

        'practice_intro': "Prem el botó per obtenir un pilot aleatori i intenta endevinar-lo.",
        'practice_button': "🎲 Nou pilot",
        'practice_title': "Mode pràctica",
        'practice_guess': "🔎 Quin pilot és?",

        'practice_correct': "✅ Correcte!",
        'practice_wrong': "❌ Incorrecte",
        'practice_show_answer': "👀 Mostrar resposta",
        'practice_answer': "🧠 {name}",

        'repte_tab': "⏱️ Repte 10/10",
        'repte_title': "⏱️ Repte 10/10",
        'repte_intro': "Tens 2 minuts per encertar 10 pilots. Pots avançar i retrocedir entre els pilots.",
        'repte_start': "🚀 Començar repte",
        'repte_next': "➡️ Següent",
        'repte_previous': "⬅️ Anterior",
        'repte_finish': "🏁 Finalitzar repte",
        'repte_question': "Pilot {current} de {total}",
        'repte_time': "⏱️ Temps restant: {time}",
        'repte_correct': "✅ Correcte!",
        'repte_wrong': "❌ No és correcte, torna-ho a provar!",
        'repte_finished': "🏁 Repte finalitzat!",
        'repte_results': "📊 Resultats",
        'repte_hits': "Encerts",
        'repte_errors': "Errors",
        'repte_unanswered': "Sense respondre",
        'repte_total_time': "Temps total",
        'repte_restart': "🔄 Tornar a jugar",
        'repte_timeout': "⏰ S'ha acabat el temps!",
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
        'tab_daily': "🏍️ Rider of the Day",
        'tab_practice': "🎲 Practice Mode",

        'practice_intro': "Press the button to get a random rider and try to guess who it is.",
        'practice_button': "🎲 New rider",
        'practice_title': "Practice Mode",
        'practice_guess': "🔎 Which rider is it?",

        'practice_correct': "✅ Correct!",
        'practice_wrong': "❌ Incorrect",
        'practice_show_answer': "👀 Show answer",
        'practice_answer': "🧠 {name}",

        'repte_tab': "⏱️ 10/10 Challenge",
        'repte_title': "⏱️ 10/10 Challenge",
        'repte_intro': "You have 2 minutes to guess 10 riders. You can move forwards and backwards between riders.",
        'repte_start': "🚀 Start challenge",
        'repte_next': "➡️ Next",
        'repte_previous': "⬅️ Previous",
        'repte_finish': "🏁 Finish challenge",
        'repte_question': "Rider {current} of {total}",
        'repte_time': "⏱️ Time remaining: {time}",
        'repte_correct': "✅ Correct!",
        'repte_wrong': "❌ Incorrect, try again!",
        'repte_finished': "🏁 Challenge finished!",
        'repte_results': "📊 Results",
        'repte_hits': "Correct",
        'repte_errors': "Errors",
        'repte_unanswered': "Unanswered",
        'repte_total_time': "Total time",
        'repte_restart': "🔄 Play again",
        'repte_timeout': "⏰ Time is up!",
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
        'tab_daily': "🏍️ Piloto del día",
        'tab_practice': "🎲 Modo práctica",

        'practice_intro': "Pulsa el botón para obtener un piloto aleatorio e intenta adivinar quién es.",
        'practice_button': "🎲 Nuevo piloto",
        'practice_title': "Modo práctica",
        'practice_guess': "🔎 ¿Qué piloto es?",

        'practice_correct': "✅ ¡Correcto!",
        'practice_wrong': "❌ Incorrecto",
        'practice_show_answer': "👀 Mostrar respuesta",
        'practice_answer': "🧠 {name}",

        'repte_tab': "⏱️ Reto 10/10",
        'repte_title': "⏱️ Reto 10/10",
        'repte_intro': "Tienes 2 minutos para acertar 10 pilotos. Puedes avanzar y retroceder entre los pilotos.",
        'repte_start': "🚀 Empezar reto",
        'repte_next': "➡️ Siguiente",
        'repte_previous': "⬅️ Anterior",
        'repte_finish': "🏁 Finalizar reto",
        'repte_question': "Piloto {current} de {total}",
        'repte_time': "⏱️ Tiempo restante: {time}",
        'repte_correct': "✅ ¡Correcto!",
        'repte_wrong': "❌ ¡Incorrecto! ¡Prueba de nuevo!",
        'repte_finished': "🏁 ¡Reto finalizado!",
        'repte_results': "📊 Resultados",
        'repte_hits': "Aciertos",
        'repte_errors': "Errores",
        'repte_unanswered': "Sin responder",
        'repte_total_time': "Tiempo total",
        'repte_restart': "🔄 Volver a jugar",
        'repte_timeout': "⏰ ¡Se ha acabado el tiempo!",
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

_pilot_del_dia(pilots):
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

# =====================================================
# FUNCIONS - REPTE 10/10
# =====================================================

REPTE_TOTAL = 10
REPTE_TEMPS = 120  # 2 minuts = 120 segons


def iniciar_repte():
    # Seleccionem 10 pilots aleatoris sense repetir
    if len(pilots) < REPTE_TOTAL:
        st.error(
            f"Calen almenys {REPTE_TOTAL} pilots al pilots.csv per poder jugar."
        )
        return

    seleccio = pilots.sample(
        n=REPTE_TOTAL,
        replace=False
    ).reset_index(drop=True)

    st.session_state.repte_pilots = seleccio
    st.session_state.repte_index = 0

    # Resultats:
    # None = sense respondre
    # True = encertat
    # False = error
    st.session_state.repte_resultats = [None] * REPTE_TOTAL

    # Respostes introduïdes per l'usuari
    st.session_state.repte_respostes = [""] * REPTE_TOTAL

    # Control del temps
    st.session_state.repte_inici = time.time()
    st.session_state.repte_final = False
    st.session_state.repte_temps_final = None


def finalitzar_repte():
    if st.session_state.repte_final:
        return

    inici = st.session_state.repte_inici
    temps_transcorregut = time.time() - inici

    st.session_state.repte_temps_final = min(
        temps_transcorregut,
        REPTE_TEMPS
    )

    st.session_state.repte_final = True


def temps_restant_repte():
    if "repte_inici" not in st.session_state:
        return REPTE_TEMPS

    temps_passat = time.time() - st.session_state.repte_inici

    return max(
        0,
        int(REPTE_TEMPS - temps_passat)
    )

@st.fragment(run_every="1s")
def mostrar_temporitzador_repte():

    if (
        "repte_inici" not in st.session_state
        or st.session_state.get("repte_final", False)
    ):
        return

    restant = temps_restant_repte()

    if restant <= 0:
        finalitzar_repte()
        st.rerun()

    minuts = restant // 60
    segons = restant % 60

    # Canviem l'estil quan queda poc temps
    if restant <= 15:
        border = "3px solid red"
    elif restant <= 30:
        border = "3px solid orange"
    else:
        border = "2px solid"

    st.markdown(
        f"""
        <div style="
            text-align:center;
            font-size:32px;
            font-weight:bold;
            padding:12px;
            border-radius:10px;
            border:{border};
            margin-bottom:15px;
        ">
            ⏱️ {minuts:02d}:{segons:02d}
        </div>
        """,
        unsafe_allow_html=True
    )


def format_temps(segons):
    minuts = int(segons // 60)
    segons_restants = int(segons % 60)

    return f"{minuts:02d}:{segons_restants:02d}"


def repte_completat():
    return all(
        resultat is not None
        for resultat in st.session_state.repte_resultats
    )

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

tab1, tab2, tab3 = st.tabs([
    translations[st.session_state.lang]['tab_daily'],
    translations[st.session_state.lang]['repte_tab'],
    translations[st.session_state.lang]['tab_practice']
])

# =====================================================
# TAB 1 - PILOT DEL DIA
# =====================================================
with tab1:

    image_path = BASE_DIR / "Fotos" / pilot_dia["image"]

    if image_path.exists():
        st.image(image_path, width="stretch")
    else:
        st.error(
            translations[st.session_state.lang]['error_image_not_found'].format(
                image=pilot_dia["image"]
            )
        )
        st.write(
            translations[st.session_state.lang]['image_path_attempted'],
            image_path,
        )

    guess = st.text_input(
        translations[st.session_state.lang]['guess_placeholder'],
        key="guess_dia"
    )

    if guess:
        if normalitza(guess) == normalitza(pilot_dia["name"]):
            st.success(
                translations[st.session_state.lang]['success_message']
            )
            st.balloons()
        else:
            st.error(
                translations[st.session_state.lang]['error_wrong_guess']
            )

    if st.button(
        translations[st.session_state.lang]['show_answer_button'],
        key="mostrar_resposta_dia"
    ):
        st.info(
            translations[st.session_state.lang]['answer_reveal'].format(
                name=pilot_dia["name"]
            )
        )

# =====================================================
# TAB 2 - MODE PRÀCTICA
# =====================================================
with tab2:

    st.write(
    translations[st.session_state.lang]['practice_intro']
)

    if st.button(
    translations[st.session_state.lang]['practice_button'],
    key="nou_pilot"
):

        st.session_state.pilot_random = obtenir_pilot_random()

        # Esborrem la resposta anterior
        if "guess_random" in st.session_state:
            del st.session_state["guess_random"]

    if "pilot_random" in st.session_state:

        pilot = st.session_state.pilot_random

        image_path = BASE_DIR / "Fotos" / pilot["image"]

        if image_path.exists():
            st.image(image_path, width="stretch")

        resposta = st.text_input(
           translations[st.session_state.lang]['practice_guess'],
            key="guess_random"
        )

        if resposta:

            if normalitza(resposta) == normalitza(pilot["name"]):
                st.success(
                    translations[st.session_state.lang]['practice_correct']
                )
            else:
                st.error(
                    translations[st.session_state.lang]['practice_wrong']
                )

        if st.button(
            "👀 Mostrar resposta",
            key="mostrar_random"
        ):
            st.info(
                translations[st.session_state.lang]['practice_answer'].format(
                name=pilot["name"]
            )
        )


# =====================================================
# TAB 3 - REPTE 10/10
# =====================================================

with tab3:

    t = translations[st.session_state.lang]

    # -------------------------------------------------
    # INICI DEL REPTE
    # -------------------------------------------------

    if "repte_pilots" not in st.session_state:

        st.subheader(t['repte_title'])

        st.write(t['repte_intro'])

        st.info("⏱️ 02:00")

        if st.button(
            t['repte_start'],
            key="iniciar_repte"
        ):
            iniciar_repte()
            st.rerun()

    # -------------------------------------------------
    # REPTE EN CURS
    # -------------------------------------------------

    elif not st.session_state.repte_final:

        # ---------------------------------------------
        # TEMPORITZADOR
        # ---------------------------------------------

        mostrar_temporitzador_repte()

        # ---------------------------------------------
        # PILOT ACTUAL
        # ---------------------------------------------

        index = st.session_state.repte_index

        pilot = st.session_state.repte_pilots.iloc[index]

        st.subheader(
            t['repte_question'].format(
                current=index + 1,
                total=REPTE_TOTAL
            )
        )

        # ---------------------------------------------
        # IMATGE
        # ---------------------------------------------

        image_path = BASE_DIR / "Fotos" / pilot["image"]

        if image_path.exists():

            st.image(
                image_path, width="stretch"
            )

        else:

            st.error(
                t['error_image_not_found'].format(
                    image=pilot["image"]
                )
            )

        # ---------------------------------------------
        # RESPOSTA
        # ---------------------------------------------

        resposta = st.text_input(
            t['guess_placeholder'],
            key=f"repte_guess_{index}"
        )

        # Guardem la resposta
        st.session_state.repte_respostes[index] = resposta

        # ---------------------------------------------
        # COMPROVAR RESPOSTA
        # ---------------------------------------------

        if resposta:

            correcta = (
                normalitza(resposta)
                == normalitza(pilot["name"])
            )

            st.session_state.repte_resultats[index] = correcta

            if correcta:

                st.success(
                    t['success_message']
                )

            else:

                st.error(
                    t['error_wrong_guess']
                )

        # ---------------------------------------------
        # NAVEGACIÓ
        # ---------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            if index > 0:

                if st.button(
                    t['repte_previous'],
                    key=f"repte_previous_{index}"
                ):

                    st.session_state.repte_index -= 1
                    st.rerun()

        with col2:

            st.write(
                f"**{index + 1} / {REPTE_TOTAL}**"
            )

        with col3:

            if index < REPTE_TOTAL - 1:

                if st.button(
                    t['repte_next'],
                    key=f"repte_next_{index}"
                ):

                    st.session_state.repte_index += 1
                    st.rerun()

        # ---------------------------------------------
        # FINALITZAR MANUALMENT
        # ---------------------------------------------

        st.divider()

        if st.button(
            t['repte_finish'],
            key="finalitzar_repte"
        ):

            finalitzar_repte()
            st.rerun()

    # -------------------------------------------------
    # RESULTATS FINALS
    # -------------------------------------------------

    else:

        st.subheader(t['repte_finished'])

        temps_final = st.session_state.repte_temps_final

        resultats = st.session_state.repte_resultats

        encerts = sum(
            resultat is True
            for resultat in resultats
        )

        errors = sum(
            resultat is False
            for resultat in resultats
        )

        sense_respondre = sum(
            resultat is None
            for resultat in resultats
        )

        # ---------------------------------------------
        # RESUM
        # ---------------------------------------------

        st.subheader(t['repte_results'])

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                t['repte_hits'],
                encerts
            )

        with col2:
            st.metric(
                t['repte_errors'],
                errors
            )

        with col3:
            st.metric(
                t['repte_unanswered'],
                sense_respondre
            )

        with col4:
            st.metric(
                t['repte_total_time'],
                format_temps(temps_final)
            )

        # ---------------------------------------------
        # AVÍS SI S'HA ACABAT EL TEMPS
        # ---------------------------------------------

        if temps_final >= REPTE_TEMPS:

            st.warning(
                t['repte_timeout']
            )

        # ---------------------------------------------
        # LLISTA DE PILOTS
        # ---------------------------------------------

        st.divider()

        for i, pilot in st.session_state.repte_pilots.iterrows():

            resultat = st.session_state.repte_resultats[i]

            if resultat is True:

                st.markdown(
                    f"""
                    <div style="
                        padding:10px;
                        margin:5px 0;
                        border-radius:8px;
                        background-color:#d4edda;
                        color:#155724;
                    ">
                        <strong>#{i + 1} — {pilot["name"]}</strong>
                        &nbsp; ✅
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif resultat is False:

                st.markdown(
                    f"""
                    <div style="
                        padding:10px;
                        margin:5px 0;
                        border-radius:8px;
                        background-color:#f8d7da;
                        color:#721c24;
                    ">
                        <strong>#{i + 1} — {pilot["name"]}</strong>
                        &nbsp; ❌
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div style="
                        padding:10px;
                        margin:5px 0;
                        border-radius:8px;
                        background-color:#eeeeee;
                        color:#555555;
                    ">
                        <strong>#{i + 1} — {pilot["name"]}</strong>
                        &nbsp; ⚪
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # ---------------------------------------------
        # TORNAR A JUGAR
        # ---------------------------------------------

        st.divider()

        if st.button(
            t['repte_restart'],
            key="repte_restart"
        ):

            # Eliminem l'estat del repte anterior
            claus_repte = [
                key for key in st.session_state.keys()
                if key.startswith("repte_guess_")
            ]

            for key in claus_repte:
                del st.session_state[key]

            del st.session_state["repte_pilots"]
            del st.session_state["repte_index"]
            del st.session_state["repte_resultats"]
            del st.session_state["repte_respostes"]
            del st.session_state["repte_inici"]
            del st.session_state["repte_final"]
            del st.session_state["repte_temps_final"]

            st.rerun()



