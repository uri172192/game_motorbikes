from instagrapi import Client
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import random
import os
from PIL import Image

# -------------------------
# Config
# -------------------------
BASE_DIR = Path(__file__).parent

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

SESSION_FILE = BASE_DIR / "session.json"

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
        ultims.add(random.randint(0, len(pilots) - 1))

    random.seed(seed_avui)

    while True:
        idx = random.randint(0, len(pilots) - 1)
        if idx not in ultims:
            return pilots.iloc[idx]


# -------------------------
# Carregar dades
# -------------------------
pilots = pd.read_csv(BASE_DIR / "pilots.csv", sep=";")
pilot_dia = obtenir_pilot_del_dia(pilots)

image_path = BASE_DIR / "Fotos" / pilot_dia["image"]

if not image_path.exists():
    raise FileNotFoundError(f"No existeix la imatge: {image_path}")

# -------------------------
# Instagram client
# -------------------------
cl = Client()
cl.load_settings("session.json")

# 🔑 1. carregar sessió si existeix
#if SESSION_FILE.exists():
#    cl.load_settings(str(SESSION_FILE))

# 🔑 2. login segur
#try:
 #   cl.login(USERNAME, PASSWORD)
 #   cl.dump_settings(str(SESSION_FILE))  # guarda sessió nova/actualitzada
#except Exception as e:
  #  print("Login error:", e)
   # print("Intentant usar sessió existent...")

# -------------------------
# 🔧 Fix imatge (IMPORTANT)
# -------------------------
img = Image.open(image_path).convert("RGB")
fixed_path = BASE_DIR / "temp_upload.jpg"
img.save(fixed_path, quality=95)

# -------------------------
# Caption
# -------------------------
caption = f"""
🏍️ PILOT DEL DIA

Saps quin pilot és?
👇 Respon als comentaris!

--------------------------
🏍️ RIDER OF THE DAY

Do you know which rider it is?
👇 Comment below!

--------------------------
🏍️ PILOTO DEL DÍA

¿Quién es este piloto?
👇 ¡Déjalo en comentarios!

#MotoGP #SBK #Motorcycle #Riders
"""

# -------------------------
# Upload
# -------------------------

cl.photo_upload(str(fixed_path), caption=caption)

print("Publicació feta!")
