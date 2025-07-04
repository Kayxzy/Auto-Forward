#Kymang

import asyncio

from pyrogram import filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked

from Kymang import bot
from Kymang.config import *
from Kymang.modules.data import *


@bot.on_message(filters.command("users") & filters.private)
async def get_users(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    msg = await c.send_message(m.chat.id, "Tunggu Sebentar...")
    users = await get_user(c.me.id)
    await msg.edit(f"{len(users)} user")


@bot.on_message(filters.command("buser") & filters.private & filters.user(ADMINS))
async def get_users(c, m):
    if c.me.id != BOT_ID:
        return
    msg = await c.send_message(m.chat.id, "Tunggu Sebentar...")
    users = await get_user(c.me.id)
    await msg.edit(f"{len(users)} user")


@bot.on_message(filters.private & filters.command("broadcast"))
async def send_text(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if not m.reply_to_message:
        return await m.reply("`/broadcast [Reply ke pesan]`")
    query = await get_user(c.me.id)
    broadcast_msg = m.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await m.reply("Tunggu Sebentar...")
    for x in query:
        chat_id = x["user"]
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(c.me.id, chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(c.me.id, chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""

    return await pls_wait.edit(status)


@bot.on_message(filters.private & filters.command("bacot") & filters.user(ADMINS))
async def send_text(c, m):
    if c.me.id != BOT_ID:
        return
    if not m.reply_to_message:
        return await m.reply("Reply Goblok")
    query = await get_user(c.me.id)
    broadcast_msg = m.reply_to_message
    total = 0
    successful = 0
    blocked = 0
    deleted = 0
    unsuccessful = 0

    pls_wait = await m.reply("SABAR NGENTOT")
    for x in query:
        chat_id = x["user"]
        try:
            await broadcast_msg.copy(chat_id)
            successful += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.copy(chat_id)
            successful += 1
        except UserIsBlocked:
            await del_user(c.me.id, chat_id)
            blocked += 1
        except InputUserDeactivated:
            await del_user(c.me.id, chat_id)
            deleted += 1
        except:
            unsuccessful += 1
        total += 1

    status = f"""**Berhasil Mengirim pesan ke:

Berhasil: {successful}
Gagal: {unsuccessful}
Pengguna Diblokir: {blocked}
Akun Dihapus: {deleted}
Total Pengguna: {total}**"""

    return await pls_wait.edit(status)


@bot.on_message(filters.command("addadmin"))
async def add_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = int(m.command[1])
    adm = await admin_info(c.me.id, ids)
    if not adm:
        await add_admin(int(c.me.id), ids)
        await m.reply(f"User {ids} Berhasil ditambahkan menjadi admin.")
    else:
        await m.reply(f"User {ids} Sudah ada di daftar Admin.")


@bot.on_message(filters.command("deladmin"))
async def del_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = int(m.command[1])
    adm = await admin_info(c.me.id, ids)
    if adm:
        await del_admin(int(c.me.id), ids)
        await m.reply(f"User {ids} Berhasil Dihapus dari daftar Admin.")
    else:
        await m.reply(f"User {ids} Tidak terdaftar di daftar Admin.")


@bot.on_message(filters.command("listadmin"))
async def cek_admin_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    msg = "**Daftar Admin**\n\n"
    adm = await cek_admin(c.me.id)
    if adm is False:
        return await m.reply("Belum ada Admin yang terdaftar.")
    ang = 0
    for ex in adm:
        try:
            afa = f"`{ex['admin']}`"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)


@bot.on_message(filters.command("addseller") & filters.user(ADMINS))
async def add_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if not iya:
        await add_seller(int(ids))
        await m.reply(f"User {ids} Berhasil di tambahkan ke seller")
    else:
        await m.reply(f"User {ids} Sudah menjadi seller")


@bot.on_message(filters.command("delseller") & filters.user(ADMINS))
async def del_seller_sub(c, m):
    if c.me.id != BOT_ID:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Balas pesan pengguna atau berikan user_id/username."
        )
    ids = m.command[1]
    iya = await seller_info(int(ids))
    if iya:
        await del_seller(int(ids))
        await m.reply(f"{ids} Berhasil di hapus dari seller")
    else:
        await m.reply(f"{ids} Bukan bagian dari seller")


@bot.on_message(filters.private & filters.command("protect"))
async def set_protect(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    adm = await admin_info(c.me.id, m.from_user.id)
    for i in cek:
        owner = i["owner"]
    if not adm and m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "`/protect [True/False]`"
        )
    jk = m.command[1]
    if jk in ["True", "False"]:
        await add_protect(c.me.id, jk)
        await m.reply(f"Berhasil mengatur protect menjadi {jk}")
    else:
        await m.reply(f"{jk} Format salah, Gunakan `/protect [True/False]`.")


@bot.on_message(filters.command("addbutton"))
async def add_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Gunakan Format `/addbutton -100xxxx`"
        )
    ids = int(m.command[1])
    adm = await sub_info(c.me.id, ids)
    x = await get_subs(c.me.id)
    s = await max_info(c.me.id)
    if len(x) == s:
        return await m.reply(f"Batas fsub {s} telah tercapai, Silahkan Hubungi Admin untuk bantuan.")
    if not adm:
        try:
            await c.export_chat_invite_link(ids)
            await add_sub(int(c.me.id), ids)
            await m.reply(f"{ids} Berhasil ditambahkan di Fsub")
        except:
            return await m.reply(f"Maaf saya bukan admin di `{ids}`")
    else:
        await m.reply(f"{adm} Sudah menjadi admin di Fsub `{ids}`")


@bot.on_message(filters.command("delbutton"))
async def del_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    if len(m.command) < 2:
        return await m.reply(
            "Gunakan format `/delbutton -100xxxx`"
        )
    ids = int(m.command[1])
    adm = await sub_info(c.me.id, ids)
    if adm:
        await del_sub(int(c.me.id), ids)
        await m.reply(f"{ids} Telah di dihapus dari Fsub")
    else:
        await m.reply(f"{ids} Tidak ditemukan di daftar Fsub")


@bot.on_message(filters.command("listbutton"))
async def cek_sub_bot(c, m):
    if c.me.id == BOT_ID:
        return
    cek = await cek_owner(c.me.id)
    for i in cek:
        owner = i["owner"]
    if m.from_user.id != owner:
        return
    msg = "**List Fsub / Button**\n\n"
    adm = await get_subs(c.me.id)
    if adm is False:
        return await m.reply("List Kosong")
    ang = 0
    for ex in adm:
        try:
            jj = await c.get_chat(ex["sub"])
            afa = f"`{jj.id}` | {jj.title}"
            ang += 1
        except Exception:
            continue
        msg += f"{ang} › {afa}\n"
    await m.reply(msg)
