import asyncio
from telegram import Bot
import requests

# Bot token and chat ID informations
BOT_TOKEN = "7908853160:AAH9UXA7xw4bjbCW03usgmMjdmyr4bdh3L4"
CHAT_ID = "1277582834"

# Tracking crypto
THRESHOLDS = {
    "bitcoin": {"below": 1200000, "above": None},  # $30,000 altına düşerse uyarı
    "ethereum": {"below": None, "above": 2000},  # $2,000 üstüne çıkarsa uyarı
}

# A function to get crypto prices
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]["usd"]

# To send telegram message anti-senc. function
async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Check price and send message function
async def check_and_alert():
    try:
        for crypto, thresholds in THRESHOLDS.items():
            price = get_crypto_price(crypto)
            print(f"{crypto.capitalize()} Fiyatı: ${price}")

            # Check important conditions
            if thresholds["below"] is not None and price < thresholds["below"]:
                await send_telegram_message(f"Uyarı: {crypto.capitalize()} fiyatı ${price} ile eşik değerin altına düştü!")
            elif thresholds["above"] is not None and price > thresholds["above"]:
                await send_telegram_message(f"Uyarı: {crypto.capitalize()} fiyatı ${price} ile eşik değerin üstüne çıktı!")
    except Exception as e:
        print(f"Hata: {e}")

# Main loop
async def main():
    while True:
        await check_and_alert()
        await asyncio.sleep(60)  # Her dakika kontrol

# Run
if __name__ == "__main__":
    asyncio.run(main())
