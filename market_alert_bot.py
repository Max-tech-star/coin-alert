import requests
import os

# Umgebungsvariablen für Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# CoinGecko Global Data
cg_response = requests.get("https://api.coingecko.com/api/v3/global").json()
data = cg_response["data"]

btc_dominance = data["market_cap_percentage"]["btc"]
total_volume = data["total_volume"]["usd"]
total_market_cap = data["total_market_cap"]["usd"]

# SentiCrypt Sentiment Score
sentiment_response = requests.get("https://api.senticrypt.com/v2/history/YYYY-MM-DD.json")

# Überprüfen, ob die Antwort gültig ist
if sentiment_response.status_code == 200:
    try:
        sentiment_data = sentiment_response.json()  # Versuche, die Antwort als JSON zu laden
        sentiment_score = sentiment_data.get("mean", "N/A")  # Hole den "mean"-Wert oder setze "N/A" falls nicht vorhanden
    except requests.exceptions.JSONDecodeError:
        print("Fehler beim Decodieren der JSON-Antwort")
        sentiment_score = "N/A"
else:
    print(f"Fehler bei der API-Anfrage, Statuscode: {sentiment_response.status_code}")
    sentiment_score = "N/A"

# Crypto News API (NewsData.io)
news_api_key = os.getenv("NEWSDATA_API_KEY")
news_url = f"https://newsdata.io/api/1/news?apikey={news_api_key}&category=business&language=en&q=crypto"
news_response = requests.get(news_url).json()
articles = news_response.get("results", [])[:3]  # Top 3 Nachrichten

# Nachricht zusammenstellen
message = (
    f"📊 *Krypto Marktübersicht*\n\n"
    f"🔸 *Bitcoin-Dominanz*: {btc_dominance:.2f}%\n"
    f"🔸 *24h Handelsvolumen*: ${total_volume:,.0f}\n"
    f"🔸 *Sentiment-Score*: {sentiment_score}\n\n"
    f"📰 *Top Nachrichten:*\n"
)

for article in articles:
    title = article.get("title", "Kein Titel")
    link = article.get("link", "")
    message += f"• [{title}]({link})\n"

# Telegram-Nachricht senden
telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": message,
    "parse_mode": "Markdown"
}
requests.post(telegram_url, data=payload)
