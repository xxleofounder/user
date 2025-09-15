import asyncio
import time
import os
import re
import random
import logging
import subprocess
import yt_dlp
import lyricsgenius

import eglence

from telethon import TelegramClient, events, errors, Button
from telethon.tl.types import ChannelParticipantsAdmins, UserStatusRecently, UserStatusOnline

from Config import tagmetin, Config

tekli_calisan = []
sent_groups = set()

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = Config.API_ID
api_hash = Config.API_HASH
bot_token = Config.BOT_TOKEN
OWNER_ID = Config.OWNER_ID
botUsername = Config.BOT_USERNAME
ownerUser = Config.OWNER_USER

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

GENIUS_TOKEN = "IEr1zibeW1gnG5yS0JTRqUFzo6iiL8-fOhQXWMGOhUK74zbKYfYwm8XmcO52oGL3"

# ʀᴀsᴛɢᴇʟᴇ ᴛᴜ̈ʀ
keywords = {
    "Rap": ["rap", "hiphop", "trap", "rap Türkçe"],
    "Pop": ["pop", "slow", "pop Türkçe", "aşk"],
    "Arabesk": ["arabesk", "türk arabesk", "arabesk slow"],
    "Diger": ["türkü", "rock", "jazz", "klasik"]
}
  


@client.on(events.NewMessage(pattern=rf"^/start(@{botUsername})?$"))
async def start(event):
    user = await event.get_sender()
    first_name = user.first_name

    await event.respond(
        f"👋🏻 **Merhaba, {first_name}**\n\n"
        "📌 **Klasik etiketleme Özelliklerine sahip, Bir Etiketleme Botuyum. Çeşitli Özelliklere Sahibim.**\n\n"
        "🔔 **Komutlar ve destek için aşağıdaki butonları kullanabilirsin.**",
        buttons=[
            [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")],
            [
                Button.inline("ℹ️ Help", data="cevirme"),
                Button.url("💬 Destek", f"https://t.me/{ownerUser}")
            ]
        ],
        link_preview=False,
        reply_to=event.message.id  # İşte burası mesajı yanıt olarak gönderir
    )


@client.on(events.ChatAction)
async def handler(event):
    # Sadece bot eklendiğinde ve ekleyen kişi varsa çalışsın
    if event.user_added and (await event.get_user()).is_self and event.added_by:
        # Aynı gruba tekrar mesaj gönderilmesini engelle
        if event.chat_id in sent_groups:
            return
        sent_groups.add(event.chat_id)

        chat = await event.get_chat()
        adder = await event.get_added_by()
        firstname = adder.first_name if adder else "Birisi"

        await client.send_message(
            event.chat_id,
            f"👋🏻 **Merhaba {firstname}, beni {chat.title} grubuna eklediğin için teşekkür ederim 🥰**\n\n"
            "📌 Detaylı bilgi için aşağıdaki butonları kullanabilirsin:",
            buttons=[
                [
                    Button.url("💬 Destek", f"https://t.me/{ownerUser}"),
                    Button.inline("📖 Help", data="cevirme")
                ]
            ],
            link_preview=False
        )

# Çevirme menüsü (Help tıklanınca)
@client.on(events.CallbackQuery(data="cevirme"))
async def cevirme(event):
    await event.edit(
        "🌿 Hangi komut menüsüne erişmek istiyorsun?",
        buttons=[
            [Button.inline("🏷️ Tagger Komutları", data="tag"), Button.inline("ℹ️ Diğer Komutlar", data="diger")],
            [Button.inline("🕹️ Eğlence Komutları", data="eglence")],
            [Button.inline("⬅️ Geri Dön", data="starta")]
        ],
        link_preview=False
    )

@client.on(events.CallbackQuery(data="tag"))
async def tag_menu(event):
    await event.edit(
        tagmetin,
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )



# Diğer menüsü
@client.on(events.CallbackQuery(data="eglence"))
async def diger_menu(event):
    await event.edit(
        "🕹️ **Eğlence Komutlarım:**\n\n"
        "⇨ `/eros` - **iᴋi ᴋișiʏi ᴇșʟᴇșᴛiʀiʀ sʜiᴘʟᴇʀ**\n\n"
        "⇨ `/stahmin` - **sᴀʏɪ ᴛᴀʜᴍiɴ ᴏʏᴜɴᴜ \n`/dur` iʟᴇ iᴘᴛᴀʟ ᴇᴅᴇʙiʟiʀsiɴiᴢ**\n\n",
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )

# Diğer menüsü
@client.on(events.CallbackQuery(data="diger"))
async def diger_menu(event):
    await event.edit(
        "📚 **Diğer Komutlarım:**\n\n"
        "⇨ `/ara` - **ʏᴏᴜᴛᴜʙᴇ'ᴅᴇɴ isᴛᴇᴅiɢiɴ ᴘᴀʀçᴀʏɪ iɴᴅiʀiʀ**\n\n"
        "⇨ `/song` - **șᴀʀᴋɪ söᴢʟᴇʀiɴi ʙᴜʟᴜʀ**\n\n"
        "⇨ `/random` - **ʀᴀsᴛɢᴇʟᴇ ᴘᴀʀçᴀ öɴᴇʀiʀ**\n\n"
        "⇨ `/bots` - **ɢʀᴜᴘᴛᴀᴋi ʙᴏᴛʟᴀʀɪ ʟisᴛᴇʟᴇʀ**\n\n"
        "⇨ `/yenile` - **sᴜɴᴜᴄᴜʏᴜ ʏᴇɴiᴅᴇɴ ʙᴀșʟᴀᴛɪʀ**",
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )

@client.on(events.CallbackQuery(data="starta"))
async def starta(event):
    user = await event.get_sender()
    first_name = user.first_name

    await event.edit(
        f"👋🏻 **Merhaba, {first_name}**\n\n"
        "📌 **Klasik etiketleme Özelliklerine sahip, Bir Etiketleme Botuyum. Çeşitli Özelliklere Sahibim.**\n\n"
        "🔔 **Komutlar ve destek için aşağıdaki butonları kullanabilirsin.**",
        buttons=[
            [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")],
            [
                Button.inline("ℹ️ Help", data="cevirme"),
                Button.url("💬 Destek", f"https://t.me/{ownerUser}")
            ]
        ],
        link_preview=False
    )

@client.on(events.NewMessage(pattern=r"^/ara (.+)"))
async def ara(event):
    query = event.pattern_match.group(1)
    status = await event.reply("🎵 ᴍᴜ̈ᴢiɢ̆i ʏᴏᴜᴛᴜʙᴇ'ᴅᴇ ᴀʀɪʏᴏʀᴜᴍ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "%(title)s.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    filename = None  # dosyayi sunucuda bırakma sil

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            if not info or "entries" not in info or len(info["entries"]) == 0:
                await status.edit("❌ ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ ʙᴜ sᴇs ᴅᴏsʏᴀsɪɴɪ, ʏᴏᴜᴛᴜʙᴇᴅᴇ ʙᴜʟᴀᴍᴀᴅɪᴍ.")
                return

            video = info["entries"][0]
            title = video.get("title", "Bilinmeyen Başlık")
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
            filename = f"{safe_title}.mp3"

        await status.edit("✅ ᴘᴀʀᴄ̧ᴀʏɪ ʙᴜʟᴅᴜᴍ")
        await status.edit("📤 ᴘᴀʀᴄ̧ᴀʏɪ ɢᴏ̈ɴᴅᴇʀɪʏᴏʀᴜᴍ, ʙɪʀ sᴀɴɪʏᴇ...")

        await event.reply(file=filename, message=f"🎶 {title}")

    except Exception as e:
        await event.reply(f"❌ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)
        await status.delete()


            
@client.on(events.NewMessage(pattern="^/yenile$"))
async def yenile(event):
    # Başlangıç mesajı (YANIT)
    mesaj = await event.reply("🔄 ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʟɪʏᴏʀ: %0")

    for yuzde in range(10, 101, 10):
        await asyncio.sleep(0.5)
        await mesaj.edit(f"🔄 ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʟɪʏᴏʀ: %{yuzde}")

    try:
        ping_output = subprocess.check_output(
            ["ping", "-c", "1", "8.8.8.8"], universal_newlines=True
        )
        # Çıktıdan süreyi al
        ping_line = [line for line in ping_output.split("\n") if "time=" in line][0]
        ping_ms = ping_line.split("time=")[1].split(" ")[0]
    except Exception:
        ping_ms = "ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ, ᴘɪɴɢ ᴏ̈ʟᴄ̧ᴜ̈ʟᴍᴇᴅɪ"

    await asyncio.sleep(2)
    await mesaj.edit(
        f"✅ ʏᴇɴɪʟᴇᴍᴇ ʙɪᴛᴛɪ!! ᴘɪɴɢ: {ping_ms} ms\n"
        f"ʙᴏᴛ ᴀʀᴛɪᴋ ᴅᴀʜᴀ sᴛᴀʙɪʟ, ɪʏɪ sᴏʜʙᴇᴛʟᴇʀ.."
    )

genius = lyricsgenius.Genius(GENIUS_TOKEN, timeout=15, skip_non_songs=True)

@client.on(events.NewMessage(pattern=r"^/song (.+)"))
async def song(event):
    query = event.pattern_match.group(1)
    status = await event.reply(f"🔎 '{query}' şᴀʀᴋɪsɪɴɪɴ sᴏ̈ᴢʟᴇʀɪɴɪ ᴀʀɪʏᴏʀᴜᴍ...")

    try:
        song = genius.search_song(query)
        if song and song.lyrics:
            lyrics = song.lyrics
            if len(lyrics) > 4000: 
                lyrics = lyrics[:4000] + "\n\n[...Daha fazla söz var]"
            await event.reply(f"🎶 {song.title} - {song.artist}\n\n{lyrics}")
        else:
            await event.reply("❌ ᴜ̈ᴢɢᴜ̈ɴᴜ̈ᴍ, şᴀʀᴋɪ sᴏ̈ᴢʟᴇʀɪɴɪ ʙᴜʟᴀᴍᴀᴅɪᴍ")
    except Exception as e:
        await event.reply(f"❌ ʙɪʀ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")
    finally:
        await status.delete()


@client.on(events.NewMessage(pattern="^/random$"))
async def random_genre(event):
    buttons = [
        [Button.inline("🎤 ʀᴀᴘ", "Rap"), Button.inline("🎵 ᴘᴏᴘ", "Pop")],
        [Button.inline("🎻 ᴀʀᴀʙᴇsᴋ", "Arabesk"), Button.inline("🎶 ᴅiɢ̆ᴇʀ", "Diger")]
    ]
    await event.respond("🎲 **ᴀʀᴀɴᴀᴄᴀᴋ şᴀʀᴋɪ ᴛᴜ̈ʀᴜ̈ɴᴜ̈ sᴇᴄ̧!:**", buttons=buttons, parse_mode="md")


@client.on(events.CallbackQuery)
async def callback_random(event):
    choice = event.data.decode("utf-8")  # seçilen tür
    if choice not in keywords:
        await event.answer("❌ ʜᴀᴛᴀ: ʙɪʟɪɴᴍᴇʏᴇɴ ᴛᴜ̈ʀ")
        return

    await event.answer(f"🔎 {choice} ᴛᴜ̈ʀᴜ̈ɴᴅᴇ şᴀʀᴋɪ sᴇᴄ̧ɪʟɪʏᴏʀ...")
    query = random.choice(keywords[choice])
    status = await event.edit(f"⏳ '{query}' ᴛᴜ̈ʀᴜ̈ɴᴅᴇ ʀᴀsᴛɢᴇʟᴇ şᴀʀᴋɪ ᴀʀᴀɴɪʏᴏʀ...")

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)
            if not info or "entries" not in info or len(info["entries"]) == 0:
                await status.edit("❌ ᴏʜʜ, şᴀʀᴋɪʏɪ ʙᴜʟᴍᴀᴅɪᴍ")
                return

            video = info["entries"][0]
            title = video.get("title", "Bilinmeyen Şarkı")
            url = video.get("webpage_url")

            await status.edit(f"🎶 **ʀᴀɴᴅᴏᴍ şᴀʀᴋɪ:**\n➡️ [{title}]({url})", parse_mode="md")

    except Exception as e:
        await status.edit(f"❌ ʜᴀᴛᴀ ᴏʟᴜşᴛᴜ: {e}")  



@client.on(events.NewMessage(pattern="^/tektag ?(.*)"))
async def mentionall(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUsername}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Mesaj veya cevap kontrolü
    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        mode = "text_on_reply"
        msg = event.reply_to_msg_id
    else:
        return await event.respond(
            "⛔ ișʟᴇᴍᴇ ʙᴀșʟᴀᴍᴀᴍ içiɴ, ʙiʀ ᴍᴇᴛiɴ ʙᴇʟiʀʟᴇᴍᴇɴ ʟᴀᴢɪᴍ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece gerçek üyeleri etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Tıklanabilir mention
        if mode == "text_on_cmd":
            mention_text = f"📢 {msg}, [{usr.first_name}](tg://user?id={usr.id})"
            await client.send_message(event.chat_id, mention_text, parse_mode='md')
        else:
            mention_text = f"📢 [{usr.first_name}](tg://user?id={usr.id})"
            await client.send_message(event.chat_id, mention_text, reply_to=msg, parse_mode='md')
        
        await asyncio.sleep(2)
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global tekli_calisan
  tekli_calisan.remove(event.chat_id)

@client.on(events.NewMessage(pattern="^/tagall ?(.*)"))
async def mentionalll(event):
    global tekli_calisan

    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUsername}?startgroup=true")]],
            reply_to=event.message.id
        )

    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        mode = "text_on_reply"
        msg = event.reply_to_msg_id
    else:
        return await event.respond(
            "⛔ ișʟᴇᴍᴇ ʙᴀșʟᴀᴍᴀᴍ içiɴ, ʙiʀ ᴍᴇᴛiɴ ʙᴇʟiʀʟᴇᴍᴇɴ ʟᴀᴢɪᴍ", 
            reply_to=event.message.id
        )

    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    users_batch = []
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue

        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        users_batch.append(f"[{usr.first_name}](tg://user?id={usr.id})")

        # 5 kişi birikince mesaj gönder
        if len(users_batch) == 5:
            if mode == "text_on_cmd":
                await client.send_message(event.chat_id, f"📢 {msg} | {', '.join(users_batch)}", parse_mode='md')
            else:
                await client.send_message(event.chat_id, f"📢 {', '.join(users_batch)}", reply_to=msg, parse_mode='md')
            users_batch = []
            await asyncio.sleep(2)

    # Kalan kullanıcıları gönder
    if users_batch:
        if mode == "text_on_cmd":
            await client.send_message(event.chat_id, f"📢 {msg} | {', '.join(users_batch)}", parse_mode='md')
        else:
            await client.send_message(event.chat_id, f"📢 {', '.join(users_batch)}", reply_to=msg, parse_mode='md')


@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:
        tekli_calisan.remove(event.chat_id)

# /yetkili komutu → adminleri listeler
@client.on(events.NewMessage(pattern="^/yetkili$"))
async def tag_admins(event):
    sender = await event.get_sender()
    chat = await event.get_chat()

    # DM kontrolü
    if event.is_private:
        return await event.respond(
            "ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴɪ ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUsername}?startgroup=true")]]
        )

    # Komutu sadece adminler kullanabilir
    is_admin = False
    async for member in client.iter_participants(chat.id, filter=ChannelParticipantsAdmins):
        if member.id == sender.id:
            is_admin = True
            break
    if not is_admin:
        return await event.reply("❌ ʙᴜ ᴋᴏᴍᴜᴛ sᴀᴅᴇᴄᴇ ɢʀᴜᴘ ʏöɴᴇᴛɪᴄɪʟᴇʀ ᴋᴜʟʟᴀɴᴀʙɪʟɪʀ")

    # Adminleri al
    admins = []
    creator = None
    async for member in client.iter_participants(chat.id, filter=ChannelParticipantsAdmins):
        if member.bot:
            continue
        if getattr(member, 'creator', False):
            creator = member
        else:
            admins.append(member)

    mesaj = ""
    sayac = 1

    if creator:
        mesaj += f"{sayac}. [{creator.first_name}](tg://user?id={creator.id})\n"
        sayac += 1

    for admin in admins[:99]:
        mesaj += f"{sayac}. [{admin.first_name}](tg://user?id={admin.id})\n"
        sayac += 1

    mesaj += "\n**♦ ɢʀᴜᴘ ᴀᴅᴍiɴʟᴇʀi ʏᴜᴋᴀʀɪᴅᴀ ʟisᴛᴇʟᴇɴᴍiș'ᴅiʀ.**"
    await event.reply(mesaj)


# /bots komutu → sadece botları listeler
@client.on(events.NewMessage(pattern="^/bots$"))
async def list_bots(event):
    chat = await event.get_chat()

    # DM kontrolü
    if event.is_private:
        return await event.reply(
            "❌ ʙᴜ ᴋᴏᴍᴜᴛ sᴀᴅᴇᴄᴇ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀᴅᴀ ᴋᴜʟʟᴀɴɪʟᴀʙɪʟɪʀ",
            buttons=[[Button.url("➕ ʙᴇɴɪ ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUsername}?startgroup=true")]]
        )

    bots = []
    async for member in client.iter_participants(chat.id):
        if member.bot:
            bots.append(member)

    if not bots:
        return await event.reply("⚠️ ʙᴜ ɢʀᴜᴘᴛᴀ ʙᴏᴛ ʙᴜʟᴜɴᴍᴀᴍᴀᴋᴛᴀᴅɪʀ")

    mesaj = "🤖 **ʙᴏᴛʟᴀʀ ʟisᴛᴇʟᴇɴᴅi:**\n\n"
    for i, bot in enumerate(bots, start=1):
        mesaj += f"{i}. [{bot.first_name}](tg://user?id={bot.id})\n"

    await event.reply(mesaj)


RANDOM_MSGS = [
    "ɴᴀsɪʟsɪɴ?",
    "ɴᴀᴘɪʏᴏʀsᴜɴ?",
    "ɪʏɪ ᴍɪsɪɴ?",
    "ɴᴇ ʜᴀʙᴇʀ?",
    "ᴋᴇʏɪғʟᴇʀ ɴᴀsɪʟ?",
    "ɢᴜɴᴜɴ ɴᴀsɪʟ ɢᴇçɪʏᴏʀ?",
    "ʙᴜɢüɴ ɴᴀsɪʟsɪɴ?",
    "ᴄᴀɴɪɴ sɪᴋɪʟɪʏᴏʀ ᴍᴜ?",
    "ᴏʏᴜɴ ᴏʏɴᴀʟɪᴍ ᴍɪ?",
    "ʙɪʀ şᴇʏʟᴇʀ ᴀɴʟᴀᴛᴍᴀᴋ ɪsᴛᴇʀ ᴍɪsɪɴ?",
    "ʏᴇᴍᴇᴋ ʏᴇᴅɪɴ ᴍɪ?",
    "ᴜʏᴜᴋ ɢᴇʟɪʏᴏʀ ᴍᴜ?",
    "ᴇɴ sᴇᴠᴅɪğɪɴ şᴀʀᴋɪ ɴᴇ?",
    "ᴅɪᴢɪ ɪᴢʟɪʏᴏʀ ᴍᴜsᴜɴ?",
    "ʏᴇɴɪ ʙɪʀ ᴋᴀʙᴀʜᴀᴛ ʙᴜʟᴅᴜɴ ᴍᴜ?",
    "ɢüʟᴇᴄᴇᴋ ʙɪʀ şᴇʏ ʟᴀᴢɪᴍ ᴍɪ?",
    "sᴇɴɪ ᴏ̈ᴢʟᴇᴅɪᴍ 🙂",
    "ʜᴀʏᴀʟ ᴋᴜʀᴅᴜɴ ᴍᴜ?",
    "ɢᴇᴄᴇ ɴᴀsɪʟ ɢᴇᴄᴛɪ?",
    "ʙɪʀʟɪᴋᴛᴇ ᴄᴀʏ ɪᴄ̧ᴇʟɪᴍ ᴍɪ?",
    "ɴᴀsɪʟ ʙɪʀ ɢᴜɴ ᴏʟᴅᴜ?",
    "ᴅᴇʀsʟᴇʀɪɴ ɴᴀsɪʟ?",
    "ᴘʀᴏᴊᴇʟᴇʀ ɴᴀsɪʟ ɢɪᴅɪʏᴏʀ?",
    "ʏᴇɴɪ ʜᴇᴅᴇғʟᴇʀ ᴋᴏʏᴅᴜɴ ᴍᴜ?",
    "ᴄᴀɴɪɴ ɴᴇ ɪsᴛɪʏᴏʀ?",
    "ʙɪʀ sᴇʏ ᴍɪ ᴏ̈ɴᴇʀᴇʏɪᴍ?",
    "ɴᴇ ᴛᴀᴋɪʟɪʏᴏʀsᴜɴ?",
    "ʜᴀᴠᴀʟᴀʀ ɴᴀsɪʟ?",
    "ɢᴜ̈ʟᴜᴍsᴇʀ ᴍɪsɪɴ 🙂",
    "ʙᴇɴɪ ᴏ̈ᴢʟᴇᴅɪɴ ᴍɪ?"
]


@client.on(events.NewMessage(pattern="^/rtag ?(.*)"))
async def mentionall(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ʀᴀɴᴅᴏᴍ ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece gerçek üyeleri etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Rastgele mesaj seç
        random_text = random.choice(RANDOM_MSGS)

        # Tıklanabilir mention
        mention_text = f"📢 {random_text} [{usr.first_name}](tg://user?id={usr.id})"
        await client.send_message(event.chat_id, mention_text, parse_mode='md')
        
        await asyncio.sleep(2)
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)
    # Boş bırakıldı, kullanıcıya mesaj göndermiyor

@client.on(events.NewMessage(pattern="^/aktiftag$"))
async def aktiftag(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴀᴋᴛɪғ ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece aktif ve son görülmesi yakın olanları etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        if not (hasattr(usr, "status") and usr.status):
            continue

        if not (usr.status.__class__.__name__ in ["UserStatusRecently", "UserStatusOnline"]):
            continue  # sadece aktif ve yakın zamanlı görülenleri al

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Tıklanabilir mention
        mention_text = f"📢 [{usr.first_name}](tg://user?id={usr.id})"
        await client.send_message(event.chat_id, mention_text, parse_mode='md')
        
        await asyncio.sleep(2)

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)


gecetag_ms = [
    "İyi geceler 🌙",
    "Resimli geceler hayırlı olsun ⭐",
    "Senin gecen tatlı rüyalarla dolsun 🌌",
    "Tatlı rüyalar ve huzurlu bir gece ✨",
    "Hoş geceler, tatlı rüyalar 🌙",
    "Güzel rüyalar gör 🌌",
    "Her gece sana mutluluk getirsin 🌟",
    "Nasıl geçerse geçsin, bu gece güzel olsun 🌙",
    "Senin için huzurlu bir gece olsun 🌌",
    "Yerin rahat olsun, iyi geceler 🌙",
    "Tatlı rüyalar gör 🌠",
    "Gece harika olsun ✨",
    "Barış dolu geceler dilerim 🌙",
    "Senin için parlak rüyalar ⭐",
    "Güzel bir gece geçir 🌌",
    "Bu gece seni tatlı rüyalarla buluştursun 🌙",
    "Gece hayırlı, rüyalar dolu olsun 🌠",
    "Huzurlu ve sakin bir gece geçir 🌙",
    "Rüyaların en güzeli seninle olsun 🌌",
    "Geceyi mutlu ve keyifli geçir 🌙",
    "Tatlı rüyalara dal 🌠",
    "Huzur dolu geceler 🌙",
    "Rüyalarının en güzel anı olsun 🌌",
    "Sevdiklerinle güzel bir gece geçir 🌟",
    "Geceyi rahat ve keyifli geçir 🌙",
    "Mutlu rüyalar dilerim 🌌",
    "Düşlerin gerçek olsun 🌠",
    "Gecenin sessizliği sana huzur versin 🌙",
    "Sevgi dolu geceler 🌌",
    "Rüya gibi bir gece geçir 🌟",
    "Geceyi keyifle geçir 🌙",
    "Tatlı uykular dilerim 🌌",
    "Rüyaların en parlak yıldızı sen ol 🌠",
    "Geceyi güzel düşüncelerle kapat 🌙",
    "Huzur ve mutluluk dolu geceler 🌌",
    "Rüya gibi uykular 🌟",
    "İçin rahat olsun, iyi geceler 🌙",
    "Geceyi sevgilerle geçir 🌌",
    "Rüyaların tatlı olsun 🌠",
    "Sessiz ve sakin bir gece 🌙",
    "Mutlulukla dolu rüyalar 🌌",
    "Gecen huzur dolu olsun 🌟",
    "Rüya gibi bir uyku dilerim 🌙",
    "Tatlı rüyalar seni bulsun 🌌",
    "Geceyi sevgiyle kapat 🌠",
    "Huzurlu ve tatlı bir uyku 🌙",
    "Geceyi keyifle geçir, tatlı rüyalar 🌌",
    "Rüyaların seni mutlu etsin 🌟",
    "İyi uykular, güzel sabahlar 🌙",
    "Huzur ve sevgi dolu bir gece 🌌",
    "Gecen tatlı rüyalarla dolsun 🌠"
]

@client.on(events.NewMessage(pattern="^/gecetag ?(.*)"))
async def gecetag(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece gerçek üyeleri etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Rastgele mesaj seç
        random_text = random.choice(gecetag_ms)

        # Tıklanabilir mention
        mention_text = f"📢 {random_text} [{usr.first_name}](tg://user?id={usr.id})"
        await client.send_message(event.chat_id, mention_text, parse_mode='md')
        
        await asyncio.sleep(2)
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)

guntag_ms = [
    "Günaydın ☀️",
    "Hayırlı sabahlar 🌸",
    "Güzel bir gün dilerim 🌞",
    "Yeni gün, yeni umutlar 🌅",
    "Mutlu bir sabah geçir 🌻",
    "Enerjik ve güzel bir gün olsun 🌞",
    "Gününü keyifle geçir 🌼",
    "Hoş sabahlar ☀️",
    "Bugün harika geçsin 🌸",
    "Pozitif bir gün dilerim 🌞",
    "Sevgi dolu bir sabah 🌅",
    "İyi ve huzurlu bir gün geçir 🌻",
    "Güne gülümseyerek başla ☀️",
    "Bugün senin için güzel olsun 🌼",
    "Huzurlu ve mutlu bir gün 🌞",
    "Yeni başlangıçlar için güzel bir sabah 🌸",
    "Güne enerjik başla ☀️",
    "İçten bir gün dilerim 🌅",
    "Günaydın, harika bir gün geçir 🌻",
    "Sabahın keyfini çıkar 🌞",
    "Güzel haberlerle dolu bir gün 🌸",
    "Bugün harika fırsatlar sunsun 🌼",
    "Pozitif enerjilerle dolu bir sabah ☀️",
    "Güne güzel bir başlangıç yap 🌞",
    "Sevdiklerinle güzel bir sabah 🌅",
    "Günaydın, tatlı bir gün olsun 🌻",
    "Huzur ve mutluluk dolu bir gün 🌸",
    "İyi sabahlar, güzel rüyaların ardından 🌞",
    "Güne güzel düşüncelerle başla ☀️",
    "Bugün senin için harika geçsin 🌼",
    "Pozitif bir enerjiyle başla 🌸",
    "Günaydın, yeni fırsatlar seni bulsun 🌅",
    "Huzurlu ve keyifli bir sabah 🌞",
    "Mutlu başlangıçlar için günaydın ☀️",
    "Güzel bir gün geçirmeni dilerim 🌻",
    "Enerjik bir sabah 🌸",
    "Günaydın, neşeli bir gün olsun 🌞",
    "Sevgi ve mutlulukla dolu bir gün 🌼",
    "Bugün her şey gönlünce olsun ☀️",
    "Güne güzel bir gülümsemeyle başla 🌸",
    "Pozitif bir sabah geçir 🌞",
    "Günaydın, huzurlu bir gün dilerim 🌻",
    "Yeni gün, yeni mutluluklar 🌅",
    "Güne keyifle başla 🌼",
    "Günaydın, harika bir gün olsun ☀️",
    "Sabahın güzellikleri seninle olsun 🌸",
    "Enerji dolu bir gün geçir 🌞",
    "Mutluluk ve neşe dolu bir sabah 🌻",
    "Pozitif düşüncelerle dolu bir gün 🌸",
    "Günaydın, güzel fırsatlar seni bulsun 🌼",
    "Huzur ve sevinç dolu bir sabah ☀️",
    "Güne güzel bir başlangıç yap 🌞"
]

@client.on(events.NewMessage(pattern="^/guntag ?(.*)"))
async def guntag(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece gerçek üyeleri etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Rastgele mesaj seç
        random_text = random.choice(guntag_ms)

        # Tıklanabilir mention
        mention_text = f"📢 {random_text} [{usr.first_name}](tg://user?id={usr.id})"
        await client.send_message(event.chat_id, mention_text, parse_mode='md')
        
        await asyncio.sleep(2)
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)


sorular_ms = [
    "En son izlediğin film neydi?",
    "Favori rengin hangisi?",
    "Hiç yabancı bir ülkeye gittin mi?",
    "Kahve mi, çay mı tercih edersin?",
    "Hangi mevsimi daha çok seversin?",
    "Hayalindeki tatil nereye olurdu?",
    "En sevdiğin yemek nedir?",
    "Hiç kitap okudun mu, hangi türleri seversin?",
    "Küçükken hayalini kurduğun meslek neydi?",
    "Favori dizin veya TV programın nedir?",
    "Müzik dinlerken en çok hangi türleri tercih edersin?",
    "Hiç spor yaptın mı, hangi sporları seversin?",
    "Bilgisayar mı yoksa telefon mu?",
    "Gün içinde en çok ne ile vakit geçirirsin?",
    "En sevdiğin tatlı nedir?",
    "Seyahat etmeyi sever misin?",
    "Hiç hayvan besledin mi, hangi hayvanları?",
    "En unutulmaz anın hangisi?",
    "Hobilerin neler?",
    "Sabah insanı mısın, gece kuşu mu?",
    "En sevdiğin film türü nedir?",
    "Dünya üzerinde gitmek istediğin tek yer neresi?",
    "Favori içeceğin nedir?",
    "Küçükken favori oyuncağın neydi?",
    "En son öğrendiğin yeni şey neydi?",
    "Rüyanda en çok görmek istediğin şey nedir?",
    "Süper güçlerin olsaydı hangisini seçerdin?",
    "Hiç ekstrem spor yaptın mı?",
    "Gelecekte yapmak istediğin en büyük şey nedir?",
    "En sevdiğin meyve hangisi?",
    "Geçmişte değiştirebileceğin bir an var mı?",
    "Zamanda yolculuk yapabilseydin hangi döneme giderdin?",
    "Bir günlüğüne görünmez olsaydın ne yapardın?",
    "En tuhaf alışkanlığın nedir?",
    "Favori çizgi filmin hangisi?",
    "Hiç hayvan gibi davranmayı denedin mi?",
    "Rüyanda en saçma şeyi gördüğün oldu mu?",
    "Bir adada yalnız kalsan yanına ne alırdın?",
    "Hiç kendi kendine şarkı söyledin mi?",
    "En sevdiğin çocukluk hatıran nedir?",
    "Sihirli bir değnek olsaydı ne yapardın?",
    "Hayatında yaptığın en çılgın şey neydi?",
    "Hiç kendini bir film karakteri gibi hissettin mi?",
    "En ilginç yeteneğin nedir?",
    "Hiç geleceğini tahmin etmeye çalıştın mı?",
    "Rüyanda hiç uçtuğun oldu mu?",
    "Favori tatil anın hangisi?",
    "Hiç kendine ait bir dil uydurdun mu?",
    "En garip rüyan neydi?",
    "Bir günlüğüne hayvan olsaydın hangisi olurdun?",
    "Hiç geçmişe mektup yazmayı denedin mi?"
]

@client.on(events.NewMessage(pattern="^/stag ?(.*)"))
async def stag(event):
    global tekli_calisan

    # Özelden kullanım engelle
    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    # Yöneticileri çek
    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]

    # Admin değilse engelle
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    # Başlatan kullanıcıya bilgi ver
    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    # Sadece gerçek üyeleri etiketle
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue  # Bot ve silinmişleri atla

        # Etiketleme durdurulduysa çık
        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        # Rastgele mesaj seç
        random_text = random.choice(sorular_ms)

        # Tıklanabilir mention
        mention_text = f"📢 {random_text} [{usr.first_name}](tg://user?id={usr.id})"
        await client.send_message(event.chat_id, mention_text, parse_mode='md')
        
        await asyncio.sleep(2)
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)

emojis = [
    "📌","💫","🔥","⭐","⚡","🎯","🌟","✨","🎉","💥",
    "💎","🌈","🎈","🪐","🌸","🍀","🍎","🍇","🍒","🥳",
    "🤩","😎","🥰","💖","💛","💚","💙","💜","🖤","🤍",
    "🤯","😇","👑","🎵","🎶","🎤","🎧","🏆","🥇","🥈",
    "🥉","⚽","🏀","🏈","⚾","🎾","🏐","🏓","🎱","🏹",
    "🌞","🌝","🌛","🌜","🌚","🌕","🌖","🌗","🌘","🌑",
    "🌒","🌓","🌔","☀️","⛅","🌤️","🌦️","🌧️","⛈️","🌩️",
    "🌨️","❄️","☃️","⛄","💧","💦","☔","🌊","🍏","🍎",
    "🍐","🍊","🍋","🍌","🍉","🍇","🍓","🫐","🍈","🍒",
    "🍑","🥭","🍍","🥥","🥝","🍅","🍆","🥑","🥦","🥬",
    "🥒","🌶️","🫑","🌽","🥕","🫒","🧄","🧅","🥔","🍠",
    "🥐","🥯","🍞","🥖","🥨","🧀","🥚","🍳","🥞","🧇",
    "🥓","🥩","🍗","🍖","🌭","🍔","🍟","🍕","🥪","🥙",
    "🫔","🌮","🌯","🥗","🥘","🥫","🍝","🍜","🍲","🍛",
    "🍣","🍱","🥟","🦪","🍤","🍙","🍚","🍘","🍥","🥠",
    "🥮","🍢","🍡","🍧","🍨","🍦","🥧","🧁","🍰","🎂",
    "🍮","🍭","🍬","🍫","🍿","🧂","🍩","🍪","🌰","🥜",
    "🍯","🥛","🍼","☕","🫖","🍵","🥤","🧃","🧉","🍶",
    "🍺","🍻","🥂","🍷","🥃","🍸","🍹","🧊","🥄","🍴",
    "🍽️","🥢","🪑","🛋️","🛏️","🛁","🚿","🪒","🧴","🧼"
]

@client.on(events.NewMessage(pattern="^/etag ?(.*)"))
async def mentionalll(event):
    global tekli_calisan

    if event.is_private:
        bot_username = (await client.get_me()).username
        return await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{bot_username}?startgroup=true")]],
            reply_to=event.message.id
        )

    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.respond(
            "⚠️ üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛᴜ sᴀᴅᴇᴄᴇ ʏᴇᴛiᴋiʟi ᴋᴜʟʟᴀɴᴀʙiʟiʀ", 
            reply_to=event.message.id
        )

    if event.pattern_match.group(1):
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        msg = event.reply_to_msg_id
    else:
        return await event.respond(
            "⛔ ișʟᴇᴍᴇ ʙᴀșʟᴀᴍᴀᴍ içiɴ, ʙiʀ ᴍᴇᴛiɴ ʙᴇʟiʀʟᴇᴍᴇɴ ʟᴀᴢɪᴍ", 
            reply_to=event.message.id
        )

    sender = await event.get_sender()
    first_name = sender.first_name
    await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ʙᴀșʟᴀᴅɪ** 🟢\nʙᴀșʟᴀᴛᴀɴ: {first_name}", reply_to=event.message.id)
    
    await asyncio.sleep(3)
    tekli_calisan.append(event.chat_id)

    users_batch = []
    async for usr in client.iter_participants(event.chat_id):
        if usr.bot or usr.deleted:
            continue

        if event.chat_id not in tekli_calisan:
            await event.respond(f"**ᴇᴛiᴋᴇᴛʟᴇᴍᴇ ișʟᴇᴍi ᴅᴜʀᴅᴜ** 🔴\nᴅᴜʀᴅᴜʀᴀɴ: {first_name}", reply_to=event.message.id)
            return

        emoji = random.choice(emojis)
        users_batch.append(f"[{emoji}](tg://user?id={usr.id})")  # Sadece emoji ile etiket

        if len(users_batch) == 5:
            await client.send_message(event.chat_id, f"📢 {msg} | {' '.join(users_batch)}", parse_mode='md')
            users_batch = []
            await asyncio.sleep(2)

    if users_batch:
        await client.send_message(event.chat_id, f"📢 {msg} | {' '.join(users_batch)}", parse_mode='md')      
        
@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
    global tekli_calisan
    if event.chat_id in tekli_calisan:  # Liste kontrolü
        tekli_calisan.remove(event.chat_id)


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



print("[INFO] - 🥰 Artz , Başarıyla Aktifleştirildi...")
client.run_until_disconnected()
