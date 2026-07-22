import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random
import os
from PIL import Image
import requests

BASE_DIR = Path(__file__).parent

ACCESS_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")

# -----------------------
# Funcions del joc
# -----------------------
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
        ultims.add(random.randint(0, len(pilots) - 1))

    random.seed(seed_avui)

    while True:
        idx = random.randint(0, len(pilots) - 1)
        if idx not in ultims:
            return pilots.iloc[idx] 

# -----------------------
# Carregar dades
# -----------------------
pilots = pd.read_csv(BASE_DIR / "pilots.csv", sep=";")
pilot_dia = obtenir_pilot_del_dia(pilots)

image_url = (
    "https://uri172192.github.io/game_motorbikes/Fotos/"
    + pilot_dia["image"]
)

print(image_url)

# -----------------

caption = f"""
🏍️ RIDER OF THE DAY

Do you know which rider it is?
👇 Comment below!

--------------------------
🏍️ PILOT DEL DIA

Saps quin pilot és?
👇 Respon als comentaris!

--------------------------
🏍️ PILOTO DEL DÍA

¿Por quién es este piloto?
👇 ¡Déjalo en comentarios!

#MotoGP #SBK #moto #riders #motorbikes
"""

create_url = f"https://graph.facebook.com/v23.0/{IG_BUSINESS_ID}/media"

payload = {
    "image_url": image_url,
    "caption": caption,
    "access_token": ACCESS_TOKEN,
}

response = requests.post(create_url, data=payload)

print(response.text)

response.raise_for_status()

creation_id = response.json()["id"]

publish_url = f"https://graph.facebook.com/v23.0/{IG_BUSINESS_ID}/media_publish"

payload = {
    "creation_id": creation_id,
    "access_token": ACCESS_TOKEN,
}

response = requests.post(publish_url, data=payload)

print(response.text)

response.raise_for_status()

print("Publicació feta correctament!")
