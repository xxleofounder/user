from telethon import Button
from telethon import TelegramClient, events
from asyncio import sleep
from Config import Config
import asyncio
import subprocess
from telethon import events
import yt_dlp
import os
from telethon import events, errors
import logging
import re 
import lyricsgenius
import random
from telethon import Button, events

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = Config.API_ID
api_hash = Config.API_HASH
bot_token = Config.BOT_TOKEN
OWNER_ID = 8276543841
botUsername = "leousertaggerbot"

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

GENIUS_TOKEN = "IEr1zibeW1gnG5yS0JTRqUFzo6iiL8-fOhQXWMGOhUK74zbKYfYwm8XmcO52oGL3"

# ʀᴀsᴛɢᴇʟᴇ ᴛᴜ̈ʀ
keywords = {
    "Rap": ["rap", "hiphop", "trap", "rap Türkçe"],
    "Pop": ["pop", "slow", "pop Türkçe", "aşk"],
    "Arabesk": ["arabesk", "türk arabesk", "arabesk slow"],
    "Diger": ["türkü", "rock", "jazz", "klasik"]
}
  


@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    user = await event.get_sender()
    first_name = user.first_name

    await client.send_message(
        event.chat_id,
        f"👋🏻 **Merhaba, {first_name}**\n\n"
        "📌 **Klasik etiketleme Özelliklerine sahip, Bir Etiketleme Botuyum, Çeşitli Özelliklere Sahibim.**\n\n"
        "🔔 **Komutlar ve destek için aşağıdaki butonları kullanabilirsin.**",
        buttons=[
            [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")],
            [
                Button.inline("ℹ️ Help", data="cevirme"),
                Button.url("💬 Destek", "https://t.me/artzfounder")
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
            [Button.inline("⬅️ Geri Dön", data="starta")]
        ],
        link_preview=False
    )

# Tagger menüsü
@client.on(events.CallbackQuery(data="tag"))
async def tag_menu(event):
    await event.edit(
        "📚 **Tagger Komutlarım Aşağıda:**\n\n"
        "➪ /tag - Grup Üyelerini 5'li Şekilde 3sn aralıklı etiketler.\n"
        "➪ /yenile - Sunucuyu yeniden başlatır, hataları giderir\n\n"
        "🔻**KOMUTLARI SADECE YETKİLİ ADMİNLER KULLANABİLİR, UNUTMA!**",
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )

# Diğer menüsü
@client.on(events.CallbackQuery(data="diger"))
async def diger_menu(event):
    await event.edit(
        "📚 **Diğer Komutlar:**\n\n"
        "➪ /ara - YouTube'den müzik veya dosya indirir\n"
        "➪ /song - Şarkı sözlerini bulur\n"
        "➪ /random - Rastgele YouTube parçası atar\n"
        "➪ /yenile - Sunucuyu yeniden başlatır",
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )

@client.on(events.CallbackQuery(data="starta"))
async def starta(event):
    user = await event.get_sender()
    first_name = user.first_name

    await event.edit(
        f"👋🏻 **Merhaba, {first_name}**\n\n"
        "📌 **Klasik etiketleme Özelliklerine sahip, Bir Etiketleme Botuyum, Çeşitli Özelliklere Sahibim.**\n\n"
        "🔔 **Komutlar ve destek için aşağıdaki butonları kullanabilirsin.**",
        buttons=[
            [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")],
            [
                Button.inline("ℹ️ Help", data="cevirme"),
                Button.url("💬 Destek", "https://t.me/artzfounder")
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
    # Başlangıç mesajı
    mesaj = await event.respond("🔄 ʏᴇɴɪᴅᴇɴ ʙᴀşʟᴀᴛɪʟɪʏᴏʀ: %0")

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
    await mesaj.edit(f"✅ ʏᴇɴɪʟᴇᴍᴇ ʙɪᴛᴛɪ!! ᴘɪɴɢ: {ping_ms} ms\nʙᴏᴛ ᴀʀᴛɪᴋ ᴅᴀʜᴀ sᴛᴀʙɪʟ, ɪʏɪ sᴏʜʙᴇᴛʟᴇʀ..")


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
  if event.is_private:
    return await event.respond("**Bu komut gruplar ve kanallar için geçerlidir❗️**")
  
  admins = []
  async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
    admins.append(admin.id)
  if not event.sender_id in admins:
    return await event.respond("**Bu komutu sadace yoneticiler kullana bilir〽**")
  
  if event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.reply_to_msg_id:
    mode = "text_on_reply"
    msg = event.reply_to_msg_id
    if msg == None:
        return await event.respond("**Önceki mesajları etiket işlemi için kullanamıyorum.**")
  elif event.pattern_match.group(1) and event.reply_to_msg_id:
    return await event.respond("Başlamak için mesaj yazmalısın❗️")
  else:
    return await event.respond("**İşleme başlamam için mesaj yazmalısın**")
  
  if mode == "text_on_cmd":
    tekli_calisan.append(event.chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"**👤 - [{usr.first_name}](tg://user?id={usr.id})**"
      if event.chat_id not in tekli_calisan:
        await event.respond("**İşlem Başarıyla Durduruldu**❌")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, f"{usrtxt} {msg}")
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""
        
  
  if mode == "text_on_reply":
    tekli_calisan.append(event.chat_id)
 
    usrnum = 0
    usrtxt = ""
    async for usr in client.iter_participants(event.chat_id):
      usrnum += 1
      usrtxt += f"👤 - [{usr.first_name}](tg://user?id={usr.id})"
      if event.chat_id not in tekli_calisan:
        await event.respond("**İşlem başarıyla durduruldu**❌")
        return
      if usrnum == 1:
        await client.send_message(event.chat_id, usrtxt, reply_to=msg)
        await asyncio.sleep(2)
        usrnum = 0
        usrtxt = ""

@client.on(events.NewMessage(pattern='^(?i)/cancel'))
async def cancel(event):
  global tekli_calisan
  tekli_calisan.remove(event.chat_id)
	

print(">> 🛠️ Artz , Başarıyla Aktifleştirildi...<<")
client.run_until_disconnected()
