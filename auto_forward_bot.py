from pyrogram import Client, filters
from pyrogram.types import Message

# Konfigurasi bot
API_ID = 28657860  # Ganti dengan API ID Anda
API_HASH = "173583c77452985e538747614c0e09e7"
BOT_TOKEN = "7840250088:AAGybB0cBwPM0yxzhwm5yhc5hT01gy1Hvd0"

# Grup sumber dan channel tujuan
SOURCE_CHAT_ID = -1002324864834   # ID grup sumber
TARGET_CHANNEL_ID = -1002077476891  # ID channel tujuan

# Daftar user_id yang diizinkan
ALLOWED_USERS = [7745070536, 6886313636]  # Ganti dengan user_id owner dan admin

app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Fungsi untuk memeriksa izin akses
def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def forward_to_channel(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None

    if not user_id or not is_authorized(user_id):
        print(f"Akses ditolak untuk user_id: {user_id}")
        return  # Tidak melakukan apapun jika user tidak diizinkan

    try:
        await message.copy(TARGET_CHANNEL_ID)
        print(f"Pesan dari user {user_id} diteruskan ke channel.")
    except Exception as e:
        print(f"Error meneruskan pesan: {e}")

print("Bot aktif dengan sistem akses terbatas...")
app.run()
