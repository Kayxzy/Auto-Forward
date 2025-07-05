from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import ChatPrivileges
import re

# Konfigurasi bot
API_ID = 28657860
API_HASH = "173583c77452985e538747614c0e09e7"
BOT_TOKEN = "7351224833:AAHmt9Bp5bZjAypka9CgLQd6CCgbY9vmZs0"

# Grup sumber dan channel tujuan
SOURCE_CHAT_ID = -1002579718516
TARGET_CHANNEL_ID = -1002077476891

# Daftar user_id yang diizinkan
ALLOWED_USERS = [7745070536, 6886313636, 1718105015, 1399943740]

app = Client("auto_forward_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USERS

# Auto-forward pesan dari grup ke channel
@app.on_message(filters.chat(SOURCE_CHAT_ID))
async def forward_to_channel(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id or not is_authorized(user_id):
        print(f"Akses ditolak untuk user_id: {user_id}")
        return
    try:
        await message.copy(TARGET_CHANNEL_ID)
        print(f"Pesan dari user {user_id} diteruskan ke channel.")
    except Exception as e:
        print(f"Error meneruskan pesan: {e}")

# Hapus pesan berdasarkan message_id
@app.on_message(filters.command("d") & filters.private)
async def delete_message(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id or not is_authorized(user_id):
        await message.reply("❌ Kamu tidak punya izin untuk menghapus pesan.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("⚠️ Format salah. Gunakan: `/d <message_id>`", quote=True)
        return

    msg_id = int(parts[1])
    try:
        await client.delete_messages(chat_id=TARGET_CHANNEL_ID, message_ids=msg_id)
        await message.reply(f"✅ Pesan dengan ID `{msg_id}` berhasil dihapus.")
    except Exception as e:
        await message.reply(f"❌ Gagal menghapus pesan:\n`{e}`")

# Pin pesan berdasarkan message_id
@app.on_message(filters.command("pin") & filters.private)
async def pin_message(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id or not is_authorized(user_id):
        await message.reply("❌ Kamu tidak punya izin untuk pin pesan.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("⚠️ Format salah. Gunakan: `/pin <message_id>`", quote=True)
        return

    msg_id = int(parts[1])
    try:
        await client.pin_chat_message(chat_id=TARGET_CHANNEL_ID, message_id=msg_id, disable_notification=True)
        await message.reply(f"📌 Pesan dengan ID `{msg_id}` berhasil dipin.")
    except Exception as e:
        await message.reply(f"❌ Gagal melakukan pin pesan:\n`{e}`")

# Unpin semua pesan di channel
@app.on_message(filters.command("unpin") & filters.private)
async def unpin_specific(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id or not is_authorized(user_id):
        await message.reply("❌ Kamu tidak punya izin untuk unpin.")
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.reply("⚠️ Format salah. Gunakan: `/unpin <message_id>`", quote=True)
        return

    msg_id = int(parts[1])
    try:
        await client.unpin_chat_message(chat_id=TARGET_CHANNEL_ID, message_id=msg_id)
        await message.reply(f"📍 Pesan dengan ID `{msg_id}` berhasil di-unpin.")
    except Exception as e:
        await message.reply(f"❌ Gagal melakukan unpin:\n`{e}`")
        
print("Bot aktif: auto-forward, hapus, pin, dan unpin...")
app.run()
