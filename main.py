from pyrogram import Client, filters
from pyrogram.types import Message

# Konfigurasi bot
API_ID = 12345678  # Ganti dengan API ID Anda dari https://my.telegram.org
API_HASH = "your_api_hash_here"  # Ganti dengan API HASH Anda
BOT_TOKEN = "7840250088:AAGybB0cBwPM0yxzhwm5yhc5hT01gy1Hvd0"

# ID grup sumber dan channel tujuan
SOURCE_CHAT_ID = -1001234567890   # Ganti dengan ID grup sumber
TARGET_CHANNEL_ID = -1009876543210  # Ganti dengan ID channel tujuan

app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def forward_to_channel(client: Client, message: Message):
    try:
        await message.copy(TARGET_CHANNEL_ID)
        print(f"Pesan diteruskan: {message.text}")
    except Exception as e:
        print(f"Gagal meneruskan pesan: {e}")

print("Bot forwarding aktif...")
app.run()
