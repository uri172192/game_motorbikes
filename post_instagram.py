from instagrapi import Client
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random
import os

# -------------------------
# Config
# -------------------------
BASE_DIR = Path(__file__).parent

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")
#USERNAME = "pilot_motos24h"
#PASSWORD = "pilot_motos24h!"

# -------------------------
# Funcions
# -------------------------
def dia_del_joc():
    ara = datetime.now()

    if ara.hour < 7:
        ara -= timedelta(days=1)

    return ara.date()

def obtenir_pilot_del_dia(pilots, dies_bloqueig=30):
    avui = dia_del_joc()
    seed_avui = avui.toordinal()

    ultims = set()

    for i in range(1, dies_bloqueig + 1):
        seed_passat = (avui - timedelta(days=i)).toordinal()

        random.seed(seed_passat)
        idx = random.randint(0, len(pilots) - 1)

        ultims.add(idx)

    random.seed(seed_avui)

    while True:
        idx = random.randint(0, len(pilots) - 1)

        if idx not in ultims:
            return pilots.iloc[idx]

# -------------------------
# Carregar pilots
# -------------------------
pilots = pd.read_csv(BASE_DIR / "pilots.csv", sep=";")

pilot_dia = obtenir_pilot_del_dia(pilots)

# -------------------------
# Preparar publicació
# -------------------------
image_path = BASE_DIR / "Fotos" / pilot_dia["image"]

caption = f"""
🏍️ PILOT DEL DIA

Saps quin pilot és?

👇 Deixa la teva resposta als comentaris!

------------------------------------------
🏍️ RIDER OF THE DAY

Do you know which pilot it is? 

👇 Leave your answer in the comments!

------------------------------------------
🏍️ PILOTO DEL DÍA

¿Sabes de qué piloto se trata? 

👇 ¡Deja tu respuesta en los comentarios!


#MotoGP #Motorbike #Rider #Motos #SBK
"""

# -------------------------
# Publicar a Instagram
# -------------------------
cl = Client()

cl.login(USERNAME, PASSWORD)

cl.photo_upload(
    path=str(image_path),
    caption=caption
)

print("Publicació feta!")
