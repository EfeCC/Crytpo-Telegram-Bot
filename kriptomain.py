import asyncio
from telegram import Bot
import requests

# Bot token ve chat ID bilgileri
BOT_TOKEN = "7908853160:AAH9UXA7xw4bjbCW03usgmMjdmyr4bdh3L4"
CHAT_ID = "1277582834"

# İzlenecek kripto paralar ve eşik değerleri
THRESHOLDS = {
    "bitcoin": {"below": 1200000, "above": None},  # $30,000 altına düşerse uyarı
    "ethereum": {"below": None, "above": 2000},  # $2,000 üstüne çıkarsa uyarı
}

# Kripto para fiyatlarını almak için fonksiyon
def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]["usd"]

# Telegram mesajı göndermek için asenkron fonksiyon
async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

# Fiyatları kontrol edip uyarı gönderen fonksiyon
async def check_and_alert():
    try:
        for crypto, thresholds in THRESHOLDS.items():
            price = get_crypto_price(crypto)
            print(f"{crypto.capitalize()} Fiyatı: ${price}")

            # Belirli koşulları kontrol et
            if thresholds["below"] is not None and price < thresholds["below"]:
                await send_telegram_message(f"Uyarı: {crypto.capitalize()} fiyatı ${price} ile eşik değerin altına düştü!")
            elif thresholds["above"] is not None and price > thresholds["above"]:
                await send_telegram_message(f"Uyarı: {crypto.capitalize()} fiyatı ${price} ile eşik değerin üstüne çıktı!")
    except Exception as e:
        print(f"Hata: {e}")

# Ana döngü
async def main():
    while True:
        await check_and_alert()
        await asyncio.sleep(60)  # Her dakika kontrol

# Programı çalıştır
if __name__ == "__main__":
    asyncio.run(main())
