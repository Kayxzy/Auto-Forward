from pyrogram import Client, filters
from pyrogram.types import Message
import re

# Konfigurasi
API_ID = 28657860
API_HASH = "173583c77452985e538747614c0e09e7"
BOT_TOKEN = "7840250088:AAGybB0cBwPM0yxzhwm5yhc5hT01gy1Hvd0"

ALLOWED_USERS = [7745070536, 6886313636]

app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

@app.on_message(filters.command("hapus") & filters.private)
async def delete_message(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id or not is_authorized(user_id):
        await message.reply("❌ Kamu tidak punya izin untuk menghapus pesan.")
        return

    if len(message.command) < 2:
        await message.reply("⚠️ Format salah. Kirim: `/hapus <link_pesan>`", quote=True)
        return

    # Ekstrak link
    url = message.command[1]
    match = re.match(r"https://t\.me/([^/]+)/(\d+)", url)
    if not match:
        await message.reply("❌ Link tidak valid. Gunakan format: `https://t.me/namachannel/1234`")
        return

    channel_username = f"@{match.group(1)}"
    msg_id = int(match.group(2))

    try:
        await client.delete_messages(chat_id=channel_username, message_ids=msg_id)
        await message.reply(f"✅ Pesan berhasil dihapus dari {channel_username} dengan ID {msg_id}")
    except Exception as e:
        await message.reply(f"❌ Gagal menghapus pesan:\n`{e}`")

print("Bot aktif dengan perintah hapus via link...")
app.run()
