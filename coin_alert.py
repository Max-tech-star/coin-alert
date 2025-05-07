import feedparser
import requests
import os
import json

RSS_URL = "https://cointelegraph.com/rss"
KEYWORDS = ["solana"]
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SEEN_FILE = "seen_articles.json"

import requests

# 🔹 Bitcoin-Kurs abrufen
btc_data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur").json()
btc_price = btc_data["bitcoin"]["eur"]

# 🔹 Fear & Greed Index abrufen
fng_data = requests.get("https://api.alternative.me/fng/").json()
fng_value = fng_data["data"][0]["value"]
fng_classification = fng_data["data"][0]["value_classification"]

# 🔹 Nachricht zusammenbauen
message = (
    f"📈 Bitcoin-Kurs: {btc_price} €\n"
    f"📊 Fear & Greed Index: {fng_value} ({fng_classification})\n"
)

# 🔹 Einfache Interpretation
if int(fng_value) < 30:
    message += "😨 Der Markt hat Angst – mögliche Kaufgelegenheit?"
elif int(fng_value) > 70:
    message += "😎 Markt ist gierig – Vorsicht vor Korrektur."
else:
    message += "🤔 Neutrale Stimmung – keine klare Richtung."

# 🔹 Telegram senden
bot_token = "7700165022:AAEMkWnOXmeR-rShtqhEEL8wE8Jcp8PRtzw"
chat_id = "7772667744"
send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
requests.post(send_url, data={"chat_id": chat_id, "text": message})

