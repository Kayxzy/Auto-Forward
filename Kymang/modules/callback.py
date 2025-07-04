#Kymang

import asyncio
import importlib
import logging
import os
from datetime import datetime, timedelta
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import *

from Kymang import Bot, bot
from Kymang.config import *
from Kymang.modules import loadModule
from Kymang.modules.btn import *
from Kymang.modules.data import *
from Kymang.modules.func import *


from .start import (
    buttons2,
    cancel,
    restart,
    start_msg
)

lonte = []


logs = logging.getLogger(__name__)




@bot.on_callback_query(filters.regex("cb_admines"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        """
    <b> ☺️ Silakan Hubungi Admin Dibawah Jika Anda Membutuhkan Bantuan.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👮‍♂ Kynan", user_id=1054295664),
                    InlineKeyboardButton(text="👮‍♂ Amang", user_id=2073506739),
                ],
                [
                    InlineKeyboardButton(
                        "Kembali", callback_data="back_start"
                    ),
                ],
            ]
        ),
    )

@bot.on_callback_query(filters.regex("cb_kontol"))
async def _(_, query: CallbackQuery):
    return await query.edit_message_text(
        f"""
    <b>**Perintah Yang Tersedia**\n\n/info - Untuk melihat masa aktif bot anda\n/setdb - Untuk mengatur channel database anda\n/addadmin - Untuk menambahkan admin bot\n/deladmin - Untuk menghapus admin bot\n/listadmin - Untuk menampilkan daftar admin\n/users - Untuk cek pengguna bot\n/broadcast - Untuk kirim pesan broadcast ke pengguna bot\n/batch - Untuk membuat link lebih dari satu file\n/genlink - buat tautan untuk satu posting\n/protect [True or False] - Berguna untuk mengaktifkan privasi konten anda\n/addbutton - Untuk menambahkan force-subs grup/channel\n/delbutton - Untuk menghapus force-subs\n/listbutton - Untuk melihat daftar force-subs</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Tutup", callback_data="mmk"
                    ),
                ]
            ]
        ),
    )

@bot.on_callback_query(filters.regex("mmk"))
async def now(_, cq):
    await cq.message.delete()

@bot.on_callback_query(filters.regex("cb_tutor"))
async def _(_, callback_query: CallbackQuery):
    await callback_query.message.edit(
        text="Berikut adalah video tutorial",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Tutorial", url="https://t.me/kynansupport"
                    ),
                    InlineKeyboardButton(
                        "Support", url="https://t.me/kynansupport"
                    ),
                ],
                [
                    InlineKeyboardButton("Kembali", callback_data="back_start"),
                ],
            ]
        ),
    )


@bot.on_callback_query(filters.regex("cb_status"))
async def _(_, callback_query: CallbackQuery):
    anu = await cek_prem()
    status_text = ""
    for ex in anu:
        try:
            afa = f"`{ex['nama']}` » {ex['aktif']}"
            status_text += f"{afa}\n"
        except Exception as e:
            print(f"Error: {e}")

    text_to_send = "Sek belum jadi"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Kembali", callback_data="back_start"),
            ],
        ]
    )

    await callback_query.message.edit(
        text=text_to_send,
        reply_markup=reply_markup,
    )

@bot.on_callback_query(filters.regex("back_start"))
async def back_start_bc(c, callback_query: CallbackQuery):
    await callback_query.message.edit(
        start_msg.format(callback_query.from_user.mention, c.me.mention),
        reply_markup=InlineKeyboardMarkup(buttons2),
    )


@bot.on_callback_query(filters.regex("buat_bot"))
async def _(c, callback_query: CallbackQuery):
    if c.me.id != BOT_ID:
        return
    user_id = callback_query.from_user.id
    kymang = await cek_seller()
    if user_id not in MEMBER and user_id not in kymang:
        for X in kymang:
            await c.resolve_peer(X)
        buttons = InlineKeyboard(row_width=3)
        keyboard: List[InlineKeyboardButton] = []
        for i in range(len(kymang)):
            list_admin = f"👮🏼 ᴀᴅᴍɪɴ {i}"
            id_admin = kymang[i]
            keyboard.append(
                InlineKeyboardButton(
                    list_admin,
                    user_id=id_admin,
                )
            )
        but = [InlineKeyboardButton("Kembali", callback_data="back_start")]
        buttons.add(*keyboard + but)
        await callback_query.message.edit(
            "**Untuk mengakses fitur premium ini, Anda perlu melakukan pembelian..**\n\n**Beli sekarang untuk bisa membuat fsub premium!**",
            reply_markup=buttons,
        )
        return
    await callback_query.message.delete()
    api_id = await c.ask(
        user_id,
        "**Masukan API_ID Anda**",
        filters=filters.text,
    )
    if await cancel(callback_query, api_id.text):
        return
    try:
        api_ids = int(api_id.text)
    except ValueError:
        await api_id.reply(
            "**API ID Haruslah berupa angka.**",
            quote=True,
        )
        return
    api_hash = await c.ask(
        user_id,
        "**Silahkan masukkan API HASH anda.**",
        filters=filters.text,
    )
    if await cancel(callback_query, api_hash.text):
        return
    bot_token = await c.ask(
        user_id,
        "**Silahkan Masukan Bot token Anda**",
        filters=filters.text,
    )
    if await cancel(callback_query, bot_token.text):
        return
    name_id = bot_token.text.split(":")[0]
    mang = Bot(
        name=str(name_id),
        api_id=api_ids,
        api_hash=api_hash.text,
        bot_token=bot_token.text,
    )
    try:
        mang.in_memory = False
        await mang.start()

        await c.send_message(
            user_id,
            f"**Bot Ditemukan:**\n**Nama :** {mang.me.mention}\n**ID :** {mang.me.id}\n**Username :** @{mang.me.username}",
        )
    except Exception as e:
        return await c.send_message(user_id, f"**ERROR**:\n{e}")
    channel_id = await c.ask(
        user_id,
        "**Masukan ID Channel Untuk Database, Pastikan Bot sudah menjadi admin di Channel Database\nContoh -100xxxx**",
        filters=filters.text,
    )
    if await cancel(callback_query, channel_id.text):
        return
    try:
        await mang.export_chat_invite_link(int(channel_id.text))
        await channel_id.reply(f"Channel Database Ditemukan `{channel_id.text}`", quote=True)
    except Exception:
        channel_id = await c.ask(user_id,
            f"Pastikan @{mang.me.username} adalah admin di Channel Database tersebut.\n\n Channel Database : `{channel_id.text}`\n\nMohon Masukkan Ulang !",
            filters=filters.text,
        )

    sub_id = await c.ask(
        user_id,
        "**Silakan Masukkan ID Channel Atau Grup Sebagai Force Subscribe !\n\nDan Pastikan Bot Anda Adalah Admin Di Grup/Channel Tersebut.**",
    )
    if await cancel(callback_query, sub_id.text):
        return
    try:
        if int(sub_id.text) != 0:
            await mang.export_chat_invite_link(int(sub_id.text))
            await sub_id.reply(f"Force-Subs terdeteksi `{sub_id.text}`", quote=True)
    except Exception:
        sub_id = await c.ask(user_id,
            f"Pastikan @{mang.me.username} adalah admin di Channel atau Group tersebut.\n\n Channel atau Group Saat Ini: `{sub_id.text}`\n\nMohon Masukkan Ulang !",
            filters=filters.text,
        )
    admin_id = await c.ask(
        user_id,
        "**Silakan Masukan ID Admin Untuk Bot Anda !**",
        filters=filters.text,
    )
    if await cancel(callback_query, admin_id.text):
        return
    try:
        admin_ids = int(admin_id.text)
    except ValueError:
        admin_id = await c.ask(user_id,
            "Bukan ID Pengguna Yang Valid, ID Pengguna Haruslah Berupa Integer",
            filters=filters.text,
        )
    owner_id = await c.ask(
        user_id,
        "**Silakan Masukan ID Owner Untuk Bot Anda !**",
        filters=filters.text,
    )
    if await cancel(callback_query, owner_id.text):
        return
    try:
        owner_ids = int(owner_id.text)
    except ValueError:
        owner_id = await c.ask(user_id,
            "Bukan ID Pengguna Yang Valid, ID Pengguna Haruslah Berupa Integer",
            filters=filters.text,
        )
    await c.send_message(user_id, "**Sukses Di Deploy . Silakan Tunggu Sebentar...**")
    await add_bot(str(mang.me.id), api_ids, api_hash.text, bot_token.text)
    await add_owner(mang.me.id, owner_ids, int(channel_id.text))
    await add_admin(mang.me.id, admin_ids)
    await add_sub(
        mang.me.id,
        int(sub_id.text),
    )
    time = (datetime.now() + timedelta(30)).strftime("%d-%m-%Y")
    await add_timer(mang.me.id, time)
    anu = await c.send_message(
        LOG_GRP,
        f"**Nama** : {mang.me.first_name}\n**Username** : @{mang.me.username}\n**Id**: {mang.me.id}\n**Masa Aktif** : {time}\n\n**Pembuat**: {callback_query.from_user.mention}\n**Id Pengguna**: {callback_query.from_user.id}",
    )

    await c.pin_chat_message(LOG_GRP, anu.id)
    sinting = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Aktif Anjeng", callback_data=f"telah_aktif {callback_query.from_user.id} {mang.me.username}"
                )
            ]
        ]
    )
    await c.send_message(LOG_GRP, f"Pesan untuk deployer @{mang.me.username}", reply_markup=sinting
    )
    os.popen(f"rm {name_id}*")
    for mod in loadModule():
            importlib.reload(importlib.import_module(f"Kymang.modules.{mod}"))
    await c.send_message(user_id, "**Bot Fsub Anda Sudah Aktif Dan Bisa Langsung Digunakan !\n\nKetik /help Di Bot Anda Untuk Melihat Perintah Yang Tersedia .\n\nTerima Kasih ...**")


@bot.on_callback_query(filters.regex("support"))
async def _(c, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    try:
        buttons = [
            [InlineKeyboardButton("Batal", callback_data=f"batal {user_id}")]
        ]
        pesan = await c.ask(
            user_id,
            "Kirimkan Pesan Anda, Admin akan membalas Pesan anda secepatnya.",
            reply_markup=InlineKeyboardMarkup(buttons),
            timeout=60,
        )
        await c.send_message(
            user_id, "✅ Pesan Anda Telah Dikirim Ke Admin, Silahkan Tunggu Balasannya"
        )
        await callback_query.message.delete()
    except asyncio.TimeoutError:
        return await c.send_message(user_id, "**Pembatalan otomatis**")
    button = [
        [
            InlineKeyboardButton(full_name, user_id=user_id),
            InlineKeyboardButton("Jawab", callback_data=f"jawab_pesan {user_id}"),
        ],
    ]
    await pesan.copy(
        LOG_GRP,
        reply_markup=InlineKeyboardMarkup(button),
    )


@bot.on_callback_query(filters.regex("jawab_pesan"))
async def _(c, callback_query: CallbackQuery):
    user_id = int(callback_query.from_user.id)
    user_ids = int(callback_query.data.split()[1])
    full_name = f"{callback_query.from_user.first_name} {callback_query.from_user.last_name or ''}"
    if user_ids == LOG_GRP:
        try:
            button = [
                [InlineKeyboardButton("Batal", callback_data=f"batal {user_id}")]
            ]
            pesan = await c.ask(
                user_id,
                "Silahkan Kirimkan Balasan Anda.",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                user_id,
                "✅ Pesan Anda Telah Dikirim Ke Admin, Silahkan Tunggu Balasannya",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(user_id, "**Pembatalkan otomatis**")
        buttons = [
            [
                InlineKeyboardButton(full_name, user_id=user_id),
                InlineKeyboardButton("Jawab", callback_data=f"jawab_pesan {user_id}"),
            ],
        ]
    else:
        try:
            button = [
                [InlineKeyboardButton("Batal", callback_data=f"batal {LOG_GRP}")]
            ]
            pesan = await c.ask(
                LOG_GRP,
                "Silahkan Kirimkan Balasan Anda.",
                reply_markup=InlineKeyboardMarkup(button),
                timeout=60,
            )
            await c.send_message(
                LOG_GRP,
                "✅ Pesan Anda Telah Dikirim Ke User, Silahkan Tunggu Balasannya",
            )
            await callback_query.message.delete()
        except asyncio.TimeoutError:
            return await c.send_message(LOG_GRP, "**Pembatalkan otomatis**")
        buttons = [
            [
                InlineKeyboardButton("Jawab", callback_data=f"jawab_pesan {LOG_GRP}"),
            ],
        ]

    await pesan.copy(
        user_ids,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("batal"))
async def _(client, callback_query: CallbackQuery):
    user_ids = int(callback_query.data.split()[1])
    if user_ids == LOG_GRP:
        client.cancel_listener(LOG_GRP)
        await client.send_message(LOG_GRP, "**Pesan di batalkan**")
    else:
        client.cancel_listener(user_ids)
        await client.send_message(user_ids, "**Pesan di batalkan**")
    await callback_query.message.delete()
    return True




@bot.on_callback_query(filters.regex("bck_cb"))
async def _(c, query: CallbackQuery):
    buttons = await button_pas_pertama(c)
    await query.message.edit(
            f"**Hello {query.from_user.mention}**\n\n**Saya dapat menyimpan file pribadi di Channel Tertentu dan pengguna lain dapat mengaksesnya dari link khusus.**",
            reply_markup=InlineKeyboardMarkup(buttons),
    )


@bot.on_callback_query(filters.regex("telah_aktif"))
async def _(client, callback_query: CallbackQuery):
    user_ids = int(callback_query.data.split()[1])
    bot_user = callback_query.data.split()[2]
    await client.send_message(user_ids, f"✅ Bot kamu telah aktif silahkan start bot @{bot_user}")
    await callback_query.message.edit("**Pesan telah di kirim**")


@bot.on_callback_query(filters.regex("tutup"))
async def cb_tutup(c, query: CallbackQuery):
    try:
        await query.answer()
        await query.message.delete()
    except BaseException as e:
        logs.info(e)
