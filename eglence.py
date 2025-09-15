from telethon import events, Button
from bot import client
import asyncio

import time
import re
import random
from telethon import TelegramClient, events, errors, Button
from telethon.tl.types import ChannelParticipantsAdmins, UserStatusRecently, UserStatusOnline


@client.on(events.NewMessage(pattern="^/eros ?(.*)"))
async def eros(event):
    bot_username = (await client.get_me()).username

    # Grup dışında kullanım kontrolü
    if event.is_private:
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUserName}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Grup kullanıcılarını al
    participants = [u async for u in client.iter_participants(event.chat_id) if not u.bot and not u.deleted]

    # Eğer yanıt varsa
    if event.reply_to_msg_id:
        replied_msg = await event.get_reply_message()
        target = replied_msg.sender
        user1 = event.sender
        user2 = target
    else:
        # Yanıt yoksa rastgele 2 kişi seç
        if len(participants) < 2:
            return await event.respond("⚠️ ʏᴇᴛᴇʀʟi ᴋᴜʟʟᴀɴɪᴄɪ ʏᴏᴋ!")
        user1, user2 = random.sample(participants, 2)

    # Eros mesajı ve emoji
    emojis = ["💖","💕","💘","💞","💓","💗","💝","💟","❣️"]
    emoji = random.choice(emojis)

    # Aşk mesajı listesi
    love_messages = [
        "**Aşk dolu bir an yaşadınız!** 😍",
        "**Kalpler bir araya geldi** 💞",
        "**Romantik bir sürpriz!** 💖",
        "**Sevgi dolu bir Eros geldi!** 💘",
        "**Kalpler birbirine dokundu** ❤️"
    ]
    love_msg = random.choice(love_messages)

    # Tıklanabilir isimlerle mesaj
    msg_text = f"{emoji} [{user1.first_name}](tg://user?id={user1.id}) ❤️ [{user2.first_name}](tg://user?id={user2.id}) {emoji}\n{love_msg}"

    # Mesajı gönder
    await event.respond(msg_text, reply_to=event.message.id, parse_mode='md')


tahmin_aktif = {} 

# Oyunu başlat
async def oyun_baslat(event, edit_msg=None):
    chat_id = event.chat_id

    sayi = random.randint(1, 1000)
    if chat_id in tahmin_aktif:
        if tahmin_aktif[chat_id]["task"]:
            tahmin_aktif[chat_id]["task"].cancel()

    tahmin_aktif[chat_id] = {"sayi": sayi, "deneme": 0, "task": None, "msg_id": None}

    text = "🎲 1-1000 arasında bir sayı tuttum! Tahminini chat'e yazabilirsin.\n\n⏳ Eğer 3 dakika boyunca kimse yazmazsa oyun otomatik bitecek."

    if edit_msg:
        await edit_msg.edit(text, buttons=None)
        tahmin_aktif[chat_id]["msg_id"] = edit_msg.id
    else:
        msg = await event.respond(text)
        tahmin_aktif[chat_id]["msg_id"] = msg.id

    async def auto_end():
        await asyncio.sleep(180)
        if chat_id in tahmin_aktif:
            del tahmin_aktif[chat_id]
            await event.respond("⏰ 3 dakika boyunca tahmin gelmedi, Oyun otomatik olarak sona erdi!")

    tahmin_aktif[chat_id]["task"] = asyncio.create_task(auto_end())

# /sayıtahmin komutu
@client.on(events.NewMessage(pattern="^/stahmin"))
async def sayi_tahmin(event):
    if event.is_private:  # DM'de çalışmayı engelle
        bot = await client.get_me()
        bot_username = bot.username
        await event.respond(
            "🤖 Beni gruba ekleyerek sayı tahmin oyununu oynayabilirsiniz!",
            buttons=[
                [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")]
            ],
            reply_to=event.message.id  # reply olarak göndersin
        )
        return
    await oyun_baslat(event)

# Tahmin kontrol
@client.on(events.NewMessage)
async def tahmin_kontrol(event):
    if event.is_private:  # DM'de çalışmayı engelle
        await event.respond(
            "🤖 Beni gruba ekleyerek sayı tahmin oyununu oynayabilirsiniz!",
            buttons=[
                [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")]
            ],
            reply_to=event.message.id  # reply olarak göndersin
        )
        return

    chat_id = event.chat_id
    if chat_id not in tahmin_aktif:
        return

    try:
        tahmin = int(event.text)
    except ValueError:
        return

    tahmin_aktif[chat_id]["deneme"] += 1
    sayi = tahmin_aktif[chat_id]["sayi"]
    deneme = tahmin_aktif[chat_id]["deneme"]

    # Görev reset
    if tahmin_aktif[chat_id]["task"]:
        tahmin_aktif[chat_id]["task"].cancel()
        async def auto_end():
            await asyncio.sleep(180)
            if chat_id in tahmin_aktif:
                del tahmin_aktif[chat_id]
                await event.respond("⏰ 3 dakika boyunca tahmin gelmedi, Oyun otomatik olarak sona erdi!")
        tahmin_aktif[chat_id]["task"] = asyncio.create_task(auto_end())
    if tahmin < sayi:
        await event.respond("🔺 ᴅᴀʜᴀ ʏüᴋsᴇᴋ ʙiʀ sᴀʏɪ söʏʟᴇ!", reply_to=event.message.id)
    elif tahmin > sayi:
        await event.respond("🔻 ᴅᴀʜᴀ ᴅüșüᴋ ʙiʀ sᴀʏɪ söʏʟᴇ!", reply_to=event.message.id)
    else:
        sender = await event.get_sender()
        msg_text = (
            f"🎉 Tebrikler! Doğru sayı **{sayi}** idi.\n"
            f"Bulan kişi: [{sender.first_name}](tg://user?id={sender.id})\n"
            f"Deneme sayısı: {deneme}"
        )

        if tahmin_aktif[chat_id]["task"]:
            tahmin_aktif[chat_id]["task"].cancel()
        del tahmin_aktif[chat_id]

        await event.respond(
            msg_text,
            buttons=[[Button.inline("🎲 Yeni Oyun", b"yeni_oyun")]],
            parse_mode='md',
            reply_to=event.message.id
        )

# Inline button callback
@client.on(events.CallbackQuery(pattern=b"yeni_oyun"))
async def yeni_oyun(event):
    if event.is_private:  # DM'de çalışmayı engelle
        await event.respond(
            "🤖 Beni gruba ekleyerek sayı tahmin oyununu oynayabilirsiniz!",
            buttons=[
                [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")]
            ],
            reply_to=event.message.id  # reply olarak göndersin
        )
        return
    try:
        await event.answer()  # butona tıklama efekti
        await oyun_baslat(event, edit_msg=await event.get_message())
    except Exception as e:
        await event.respond(f"⚠️ Hata: {e}", reply_to=event.message.id)

# /dur komutu
@client.on(events.NewMessage(pattern="^/dur"))
async def oyun_dur(event):
    if event.is_private:  # DM'de çalışmayı engelle
        await event.respond(
            "🤖 Beni gruba ekleyerek sayı tahmin oyununu oynayabilirsiniz!",
            buttons=[
                [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")]
            ],
            reply_to=event.message.id  # reply olarak göndersin
        )
        return

    chat_id = event.chat_id
    if chat_id in tahmin_aktif:
        if tahmin_aktif[chat_id]["task"]:
            tahmin_aktif[chat_id]["task"].cancel()
        del tahmin_aktif[chat_id]
        await event.respond("🔴 sᴀʏɪ ᴛᴀʜᴍiɴ ᴏʏᴜɴᴜ, ʙᴀșᴀʀɪʏʟᴀ ᴅᴜʀᴅᴜʀᴜʟᴅᴜ!", reply_to=event.message.id)
                
