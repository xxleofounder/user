import asyncio
import time
import os
import re
import random
import logging
import subprocess
import yt_dlp
import lyricsgenius
from datetime import datetime
from datetime import datetime, time, timedelta

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
ADMIN_ID = Config.OWNER_ID
BOT_NAME = "funda"

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

GENIUS_TOKEN = "IEr1zibeW1gnG5yS0JTRqUFzo6iiL8-fOhQXWMGOhUK74zbKYfYwm8XmcO52oGL3"

 
# Orijinal fonksiyonları sakla
_original_send_message = client.send_message
_original_edit_message = client.edit_message

# Flood-safe send_message
async def flood_safe_send(*args, **kwargs):
    while True:
        try:
            return await _original_send_message(*args, **kwargs)
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except Exception:
            break

# Flood-safe edit_message
async def flood_safe_edit(*args, **kwargs):
    while True:
        try:
            return await _original_edit_message(*args, **kwargs)
        except errors.FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except Exception:
            break

# Fonksiyonları override et
client.send_message = flood_safe_send
client.edit_message = flood_safe_edit



funda_cevaplar = [
    "Buradayım tatlım 💖",
    "Hee aşkım, beni mi çağırdın? 😘",
    "Canım benim, senin için hep buradayım 🌸",
    "Buyur prensesim ✨",
    "Beni özledin mi yoksa? 💕",
    "Geldim aşkım 😍",
    "Tatlım, beni mi sordunuz? 🌼",
    "Sen çağırırsan gelmez miyim? 😇",
    "Şekerim, buradayım 💫",
    "Hayatım, bana mı seslendin? 💕",
    "Meleğim, senin için hep buradayım 🌸",
    "Funda burada, buyur canım 😘",
    "Sana kulaklarım her zaman açık tatlım 💖",
    "Benim güzelim, ne istedin benden 🌹",
    "Sultanım, buradayım 😍",
    "Sen benim kalbimsin 💕 buradayım",
    "Buyur balım 🌼",
    "Kime lazımım? Tatlım bana seslendi galiba 😏",
    "Benim minnoşum 💖 geldim",
    "Ruh eşim, buradayım ✨",
    "Baby, ben buradayım 😘",
    "Beni mi çağırdın güneşim 🌞",
    "Ben geldim 😍",
    "Hehe, bana mı seslendiniz? 💕",
    "Tatlışım, hep yanındayım 🌸",
    "Canım canım 💖 buradayım",
    "Beni özledin mi yoksa şekerim 😘",
    "Fıstığım 💕 ben buradayım",
    "Gönlümün sahibi, buradayım ✨",
    "Sen çağırdın, ben geldim 😍",
    "Kalbim, her daim yanındayım 💖",
    "Aşkım, tatlı sesini duydum 💕",
    "Buyurun canım 🌼",
    "Benim güzel ailem, buradayım 😘",
    "Melek gibi çağırdın, geldim 😇",
    "Benim tatlı kuşum 💕",
    "Sen iste, ben hep buradayım 🌸",
    "Buyur prensesim, emrin olur ✨",
    "Sultanım 😍 sesini duydum",
    "Benim tatlım 💖 buradayım",
    "Çiçeğim, buradayım 🌺",
    "Sen bana seslenince içim ısınıyor 💕",
    "Buyur balım, geldim 🌸",
    "Heh, tatlım, ben geldim 😇",
    "Aşkım, senin için buradayım 😘",
    "Sana hep cevap veririm tatlım 💖",
    "Ben buradayım, tatlı kalbinle çağırdın 🌼",
    "Senin yanında olmak bana huzur 💕",
    "Güzelim, bana mı seslendin 😍",
    "Funda her daim burada ✨"
]



tetikklm = ["funda", "Funda", "aşkım", "Aşkım"]

@client.on(events.NewMessage())
async def funda_cevap(event):
    if event.is_private:
        return  # DM'de cevap vermesin

    text = event.raw_text
    if any(word in text for word in tetikklm):
        cevap = random.choice(funda_cevaplar)
        await event.reply(cevap)




@client.on(events.NewMessage(pattern=rf"^/start(@{botUsername})?$"))
async def start(event):
    user = await event.get_sender()
    first_name = user.first_name
    username = f"@{user.username}" if user.username else "Yok"
    user_id = user.id

    # Kullanıcıya gönderilecek mesaj
    await event.respond(
        f"**Selam tatlım {first_name}, ben Funda 🌸**\n\n"
        "💕 **Gruptaki Kullanıcılara Etiket atabilir, grup içi oyun açabilir yada extra komutlarım ile sana yardım edebilirim. Çok çeşitli özelliklerim bulunuyor, Beni denemek istemezmisin? Aşağıdaki butonlarla beni yönetebilirsin.**\n\n"
        "🔔 **Unutma, hala gelişme aşamasındayım. beta sürümündeyim duyuruları sizlerle paylaşcağım aşklarım...**",
        buttons=[
            [Button.url("➕ Beni Gruba Ekle", f"https://t.me/{botUsername}?startgroup=true")],
            [
                Button.inline("ℹ️ Help", data="cevirme"),
                Button.url("💬 Destek", f"https://t.me/{ownerUser}")
            ]
        ],
        link_preview=False,
        reply_to=event.message.id
    )

    # Log bilgisi
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_mesaj = (
        "📥 Yeni /start Kullanımı\n\n"
        f"👤 İsim: {first_name}\n"
        f"🆔 ID: `{user_id}`\n"
        f"🔗 Username: {username}\n"
        f"🕒 Tarih/Saat: {tarih}"
    )

    # Admin'e DM gönder
    try:
        await client.send_message(ADMIN_ID, log_mesaj)
    except Exception as e:
        print(f"Sorun: {e}")


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
            f"🌸**Merhaba tatlım {firstname}, beni {chat.title} grubuna eklediğin için teşekkür ederim 🥰**\n\n"
            "⭐ Aşkım beni aşağıdaki buttonlar'dan yönetebilirsin:",
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
        "⇨ `/xox` - **iᴋi ᴋiși ᴀʀᴀsɪɴᴅᴀ xᴏx ᴏʏᴜɴᴜ**\n"
        "⇨ `/tkm` - **ʙᴏᴛʟᴀ ᴛᴀș/ᴋᴀɢɪᴛ/ᴍᴀᴋᴀs ᴏʏɴᴀ**\n"
        "⇨ `/stahmin` - **sᴀʏɪ ᴛᴀʜᴍiɴ ᴏʏᴜɴᴜ**\n\n"
        "⇨ `/eros` - **iᴋi ᴋișiʏi ᴇșʟᴇșᴛiʀiʀ, sʜiᴘʟᴇʀ**\n"
        "⇨ `/saril` - **ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ, sᴀʀɪʟ!**\n"
        "⇨ `/kiss` - **ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ, öᴘ!**\n"
        "⇨ `/kick` - **ᴀʀᴋᴀᴅᴀșɪɴɪ ɢʀᴜᴘᴛᴀɴ șᴜᴛʟᴀ! (șᴀᴋᴀ)**\n"
        "⇨ `/slap` - **ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ, ᴛᴏᴋᴀᴛʟᴀ!**\n"
        "⇨ `/dart` - **ʀᴀɴᴅᴏᴍ ᴅᴀʀᴛ ᴀᴛᴀʀ**\n"
        "⇨ `/zar` -  **ʀᴀɴᴅᴏᴍ ᴢᴀʀ ᴀᴛᴀʀ**\n"
        "⇨ `/bowling` - **ʀᴀɴᴅᴏᴍ ʙᴏᴡʟiɴɢ sᴋᴏʀᴜ**\n"
        "⇨ `/futbool` - **ʀᴀɴᴅᴏᴍ șᴜᴛ çᴇᴋᴇʀ**\n"
        "⇨ `/slot` - ** ʀᴀɴᴅᴏᴍ sʟᴏᴛ çᴇᴠiʀiʀ**\n"
        "⇨ `/coin` - ** ʀᴀɴᴅᴏᴍ ʏᴀᴢɪ/ᴛᴜʀᴀ ᴀᴛᴀʀ**\n\n"

        
        "🔻 **ᴏʏᴜɴʟᴀʀɪ, `/off` ᴋᴏᴍᴜᴛᴜ ʏᴀʀᴅɪᴍɪ iʟᴇ iᴘᴛᴀʟ ᴇᴅᴇʙiʟiʀsiɴiᴢ.**",
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
        "⇨ `/bots` - **ɢʀᴜᴘᴛᴀᴋi ʙᴏᴛʟᴀʀɪ ʟisᴛᴇʟᴇʀ**\n\n"
        "⇨ `/destek` - **ᴏᴡɴᴇʀ'ᴇ ᴜʟᴀșᴀʙiʟiʀ, ʏᴀᴅᴀ ʙᴏᴛ ʜᴀᴋᴋɪɴᴅᴀ ʙiʀ sᴏʀᴜɴᴜ ʙiʟᴅiʀᴇʙiʟiʀsiɴiᴢ**\n\n"
        "⇨ `/id` - **ʏᴀɴɪᴛ ᴠᴇʀiʀsᴇɴ ᴋișiɴiɴ ᴠᴇʀᴍᴇᴢsᴇɴ sᴇɴiɴ iᴅ ᴠᴇʀiʀ**\n\n"
        "⇨ `/info` - **ʏᴀɴɪᴛ ᴠᴇʀiʀsᴇɴ ᴋișiɴiɴ ᴠᴇʀᴍᴇᴢsᴇɴ sᴇɴiɴ ɪɴғᴏ ᴠᴇʀiʀ**\n\n"
        "⇨ `/yenile` - **sᴜɴᴜᴄᴜʏᴜ ʏᴇɴiᴅᴇɴ ʙᴀșʟᴀᴛɪʀ**",
        buttons=[[Button.inline("⬅️ Geri Dön", data="cevirme")]],
        link_preview=False
    )

@client.on(events.CallbackQuery(data="starta"))
async def starta(event):
    user = await event.get_sender()
    first_name = user.first_name

    await event.edit(
        f"**Selam tatlım {first_name}, ben Funda 🌸**\n\n"
        "💕 **Gruptaki Kullanıcılara Etiket atabilir, grup içi oyun açabilir yada extra komutlarım ile sana yardım edebilirim. Çok çeşitli özelliklerim bulunuyor, Beni denemek istemezmisin? Aşağıdaki butonlarla beni yönetebilirsin.**\n\n"
        "🔔 **Unutma, hala gelişme aşamasındayım. beta sürümündeyim duyuruları sizlerle paylaşcağım aşklarım...**",
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
        await asyncio.sleep(2)
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

games = {}

@client.on(events.NewMessage(pattern="^/stahmin"))
async def start_game(event):
    chat_id = event.chat_id

    # DM kontrolü
    if event.is_private:
        await event.respond(
            "üᴢɢüɴüᴍ, ʙᴜ ᴋᴏᴍᴜᴛ ɢʀᴜᴘ ᴠᴇʏᴀ ᴋᴀɴᴀʟʟᴀʀ içiɴ ɢᴇçᴇʀʟiᴅiʀ❗️",
            buttons=[[Button.url("➕ ʙᴇɴi ɢʀᴜʙᴀ ᴇᴋʟᴇ", f"https://t.me/{botUsername}?startgroup=true")]],
            reply_to=event.message.id
        )
        return

    # Oyun zaten aktif mi kontrolü
    if chat_id in games and games[chat_id]["active"]:
        await event.respond("⚠️ ᴏʏᴜɴ ᴢᴀᴛᴇɴ ᴀᴋᴛiғ! ᴅᴇᴠᴀᴍ ᴇᴅᴇʙiʟiʀsiɴiᴢ..", reply_to=event.id)
        return

    # Yeni sayı üret
    number = random.randint(1, 1000)
    games[chat_id] = {"number": number, "active": True, "task": None}

    await event.respond(
        f"🎯 **1-1000 ᴀʀᴀsɪ ʙiʀ sᴀʏɪ ᴀᴋʟɪᴍᴅᴀ ᴛᴜᴛᴛᴜᴍ!**\n\n"
        f"⏳ **3ᴅᴋ ʙᴏʏᴜɴᴄᴀ ʙiʀ ᴛᴀʜᴍiɴ ɢᴇʟᴍᴇᴢsᴇ ᴏʏᴜɴ ᴏᴛᴏᴍᴀᴛiᴋ iᴘᴛᴀʟ ᴏʟᴜᴄᴀᴋ, iʏi ᴏʏᴜɴʟᴀʀ...**"
    )

    games[chat_id]["task"] = asyncio.create_task(auto_end_game(chat_id))

@client.on(events.NewMessage())
async def guess_number(event):
    if event.is_private:
        return

    chat_id = event.chat_id

    if chat_id not in games or not games[chat_id]["active"]:
        return

    try:
        tahmin = int(event.raw_text)
    except ValueError:
        return

    number = games[chat_id]["number"]

    if tahmin < number:
        await event.respond(f"🔺 {event.sender.first_name}, ᴅᴀʜᴀ ʙüʏüᴋ ʙiʀ sᴀʏɪ söʏʟᴇ! ({tahmin})", reply_to=event.id)
    elif tahmin > number:
        await event.respond(f"🔻 {event.sender.first_name}, ᴅᴀʜᴀ ᴋüçüᴋ ʙiʀ sᴀʏɪ söʏʟᴇ! ({tahmin})", reply_to=event.id)
    else:
        await event.respond(
            f"🎉 Tebrikler {event.sender.first_name}! 🎊\n"
            f"🟢 ᴀᴋʟɪᴍᴅᴀᴋi sᴀʏɪ: **{number}**", reply_to=event.id
        )
        games[chat_id]["active"] = False
        if games[chat_id]["task"]:
            games[chat_id]["task"].cancel()
        await event.respond("", reply_to=event.id)

async def auto_end_game(chat_id):
    try:
        await asyncio.sleep(180)
        if chat_id in games and games[chat_id]["active"]:
            games[chat_id]["active"] = False
            await client.send_message(
                chat_id,
                "⏰ 3ᴅᴋ ʙᴏʏᴜɴᴄᴀ ᴛᴀʜᴍiɴ ɢᴇʟᴍᴇᴅi, ᴏʏᴜɴ iᴘᴛᴀʟ ᴇᴅiʟᴅi.\n"
                
            )
    except asyncio.CancelledError:
        pass

@client.on(events.NewMessage(pattern="^/off"))
async def stop_game(event):
    if event.is_private:
        return

    chat_id = event.chat_id

    if chat_id in games and games[chat_id]["active"]:
        games[chat_id]["active"] = False
        if games[chat_id]["task"]:
            games[chat_id]["task"].cancel()
        await event.respond("🔴 ᴏʏᴜɴ ᴍᴀɴᴜᴇʟ ᴏʟᴀʀᴀᴋ ᴅᴜʀᴅᴜʀᴜʟᴅᴜ, /stahmin iʟᴇ ʏᴇɴiᴅᴇɴ ʙᴀșʟᴀᴛᴀʙiʟiʀsiɴiᴢ.", reply_to=event.id)
    


xox_games = {}

def render_board(board):
    return [[Button.inline(board[r][c], data=f"xox_{r}_{c}") for c in range(len(board))] for r in range(len(board))]

def check_winner(board, symbol):
    size = len(board)
    needed = 4  

    
    for r in range(size):
        for c in range(size - needed + 1):
            if all(board[r][c+i] == symbol for i in range(needed)):
                return True


    for c in range(size):
        for r in range(size - needed + 1):
            if all(board[r+i][c] == symbol for i in range(needed)):
                return True

    
    for r in range(size - needed + 1):
        for c in range(size - needed + 1):
            if all(board[r+i][c+i] == symbol for i in range(needed)):
                return True

    
    for r in range(size - needed + 1):
        for c in range(needed - 1, size):
            if all(board[r+i][c-i] == symbol for i in range(needed)):
                return True

    return False

def check_draw(board):
    return all(cell != "⬜" for row in board for cell in row)


@client.on(events.NewMessage(pattern="^/xox"))
async def start_xox(event):
    if event.is_private:
        return  

    chat_id = event.chat_id
    if chat_id in xox_games:
        return  

    size = 6
    board = [["⬜" for _ in range(size)] for _ in range(size)]
    msg = await event.respond("🎮 xᴏx ᴏʏᴜɴᴜ ᴀᴋᴛiғ\n\n🧑 ᴏʏᴜɴᴄᴜʟᴀʀ ʙᴇᴋʟᴇɴiʏᴏʀ...", buttons=render_board(board))

    xox_games[chat_id] = {
        "board": board,
        "players": [],
        "turn": "❌",
        "msg_id": msg.id
    }


@client.on(events.CallbackQuery(pattern=r"xox_(\d+)_(\d+)"))
async def xox_move(event):
    chat_id = event.chat_id
    if chat_id not in xox_games:
        return

    game = xox_games[chat_id]
    r, c = map(int, event.data.decode().split("_")[1:])

    # Oyuncu ekleme
    if event.sender_id not in game["players"]:
        if len(game["players"]) < 2:
            game["players"].append(event.sender_id)
        else:
            return

    # Oyuncu sırası kontrolü
    if len(game["players"]) < 1:
        return

    current_player = game["players"][0 if game["turn"] == "❌" else 1]
    if event.sender_id != current_player:
        return

    # Hücre dolu mu?
    if game["board"][r][c] != "⬜":
        return

    game["board"][r][c] = game["turn"]

    # Kazanan kontrolü
    if check_winner(game["board"], game["turn"]):
        winner = await event.client.get_entity(event.sender_id)
        await event.edit(f"🎉 ᴛᴇʙʀiᴋʟᴇʀ, ᴋᴀᴢᴀɴᴀɴ: {winner.first_name}", buttons=[
            [Button.inline("🔄 ʏᴇɴi ᴏʏᴜɴ", data="restart_xox")]
        ])
        del xox_games[chat_id]
        return

    # Beraberlik kontrolü
    if check_draw(game["board"]):
        await event.edit("🤝 ᴏʏᴜɴ ʙᴇʀᴀʙᴇʀᴇ ʙiᴛᴛi!", buttons=[
            [Button.inline("🔄 ʏᴇɴi ᴏʏᴜɴ", data="restart_xox")]
        ])
        del xox_games[chat_id]
        return

    # Sıra değiştir
    game["turn"] = "⭕" if game["turn"] == "❌" else "❌"

    # Oyuncu isimleri
    player_text = ""
    if len(game["players"]) >= 1:
        p1 = await event.client.get_entity(game["players"][0])
        player_text += f"👤 1. ᴏʏᴜɴᴄᴜ: {p1.first_name}\n"
    if len(game["players"]) == 2:
        p2 = await event.client.get_entity(game["players"][1])
        player_text += f"👤 2. ᴏʏᴜɴᴄᴜ: {p2.first_name}\n\n👉 Hamle sırası: {p2.first_name if game['turn']=='⭕' else p1.first_name}"

    await event.edit(f"🎮 xᴏx ᴏʏᴜɴᴜ\n\n{player_text}", buttons=render_board(game["board"]))


@client.on(events.CallbackQuery(pattern="restart_xox"))
async def restart_xox(event):
    chat_id = event.chat_id
    size = 6
    board = [["⬜" for _ in range(size)] for _ in range(size)]
    msg = await event.edit("🎮 xᴏx ᴏʏᴜɴᴜ ᴀᴋᴛiғ\n\n🧑 ᴏʏᴜɴᴄᴜʟᴀʀ ʙᴇᴋʟᴇɴiʏᴏʀ...", buttons=render_board(board))

    xox_games[chat_id] = {
        "board": board,
        "players": [],
        "turn": "❌",
        "msg_id": msg.id
    }


@client.on(events.NewMessage(pattern="^/off$"))
async def stop_xox(event):
    chat_id = event.chat_id

    if chat_id in xox_games:
        try:
            msg_id = xox_games[chat_id]["msg_id"]
            await client.delete_messages(chat_id, msg_id) 
        except Exception:
            pass
        del xox_games[chat_id]
        await event.reply("❌ xᴏx ᴏʏᴜɴᴜ ʙᴀșᴀʀɪʏʟᴀ sᴏɴʟᴀɴᴅɪʀɪʟᴅɪ, ʏᴇɴi ᴏʏᴜɴ içiɴ `/xox` ᴋᴏᴍᴜᴛᴜɴᴜ ᴋᴜʟʟᴀɴᴀʙiʟiʀsiɴiᴢ.")    


# /tasmakas komutu (sadece grup)
@client.on(events.NewMessage(pattern="^/tkm"))
async def tasmakas_start(event):
    if event.is_private:
        await event.respond("❌ Bu oyun sadece gruplarda oynanabilir!")
        return

    buttons = [
        [Button.inline("🪨 Taş", b"tas"), Button.inline("📄 Kağıt", b"kagit"), Button.inline("✂️ Makas", b"makas")]
    ]
    await event.reply("✊ Taş, Kağıt, Makas! Seçimini yap:", buttons=buttons)

# Inline button handler
@client.on(events.CallbackQuery)
async def tasmakas_handler(event):
    
    data = event.data.decode()

    if data in ["tas", "kagit", "makas"]:
        secim = data
        bot_secim = random.choice(["tas", "kagit", "makas"])

        # Sonucu belirle
        if secim == bot_secim:
            sonuc = "🤝 Berabere!"
        elif (secim == "tas" and bot_secim == "makas") or \
             (secim == "kagit" and bot_secim == "tas") or \
             (secim == "makas" and bot_secim == "kagit"):
            sonuc = "🎉 ᴛᴇʙʀiᴋʟᴇʀ, ᴋᴀᴢᴀɴᴅɪɴɪᴢ!"
        else:
            sonuc = "💔 ᴍᴀᴀʟᴇsᴇғ ᴋᴀʏʙᴇᴛiɴiᴢ!"

        emoji_map = {"tas": "🪨 Taş", "kagit": "📄 Kağıt", "makas": "✂️ Makas"}

        # Sonuç mesajını editleyip "Yeniden Oyna" butonu ekle
        yeniden_buttons = [[
            Button.inline("🕹 ʏᴇɴiᴅᴇɴ ᴏʏɴᴀ", b"yeniden")
        ]]
        await event.edit(
            f"🧑 sᴇɴ: {emoji_map[secim]}\n🤖 ʙᴏᴛ: {emoji_map[bot_secim]}\n\n{sonuc}",
            buttons=yeniden_buttons
        )

    elif data == "yeniden":
        # Mesajı editleyip yeni oyun başlat
        buttons = [
            [Button.inline("🪨 Taş", b"tas"), Button.inline("📄 Kağıt", b"kagit"), Button.inline("✂️ Makas", b"makas")]
        ]
        await event.edit("✊ Taş, Kağıt, Makas! Seç:", buttons=buttons)



# 🎲 /zar
@client.on(events.NewMessage(pattern="^/zar$"))
async def zar(event):
    sonuc = random.randint(1, 6)
    await client.send_message(event.chat_id, f"🎲 ᴢᴀʀ sᴏɴᴜᴄᴜ: {sonuc}", reply_to=event.id)

# 🎯 /dart
@client.on(events.NewMessage(pattern="^/dart$"))
async def dart(event):
    sonuc = random.randint(1, 6)
    await client.send_message(event.chat_id, f"🎯 ᴅᴀʀᴛ sᴏɴᴜᴄᴜ: {sonuc}", reply_to=event.id)

# 🎰 /slot
@client.on(events.NewMessage(pattern="^/slot$"))
async def slot(event):
    slotlar = ["🍒", "🍋", "🍊", "🍉", "⭐"]
    sonuc = " | ".join(random.choices(slotlar, k=3))
    await client.send_message(event.chat_id, f"🎰 sʟᴏᴛ sᴏɴᴜᴄᴜ: {sonuc}", reply_to=event.id)

# ⚽ /futbool
@client.on(events.NewMessage(pattern="^/futbool$"))
async def futbool(event):
    gol = random.choice(["ɢᴏʟʟ! ⚽", "ᴛᴏᴘ ᴋᴀçᴛɪ! ❌"])
    await client.send_message(event.chat_id, gol, reply_to=event.id)

# 🎳 /bowling
@client.on(events.NewMessage(pattern="^/bowling$"))
async def bowling(event):
    skor = random.randint(0, 10)
    await client.send_message(event.chat_id, f"🎳 ʙᴏᴡʟiɴɢ sᴋᴏʀᴜ: {skor}", reply_to=event.id)

# 🪙 /coin
@client.on(events.NewMessage(pattern="^/coin$"))
async def coin(event):
    sonuc = random.choice(["🪙 ʏᴀᴢɪ", "🪙 ᴛᴜʀᴀ"])
    await client.send_message(event.chat_id, f"» {sonuc}", reply_to=event.id)

# 👋 /slap (sadece grupta)
@client.on(events.NewMessage(pattern="^/slap$"))
async def slap(event):
    if not event.is_group:
        return
    if event.is_reply:
        reply = await event.get_reply_message()
        await client.send_message(
            event.chat_id,
            f"{event.sender.first_name} {reply.sender.first_name}’i ᴛᴏᴋᴀᴛʟᴀᴅɪ!",
            reply_to=event.id
        )
    else:
        await client.send_message(event.chat_id, "ʙiʀisiɴi ᴛᴏᴋᴀᴛʟᴀᴍᴀᴋ içiɴ ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ!", reply_to=event.id)

# 👢 /kick (sadece grupta)
@client.on(events.NewMessage(pattern="^/kick$"))
async def kick(event):
    if not event.is_group:
        return
    if event.is_reply:
        reply = await event.get_reply_message()
        await client.send_message(
            event.chat_id,
            f"{event.sender.first_name} {reply.sender.first_name}’i ɢʀᴜᴘᴛᴀɴ ᴀᴛᴛɪ!",
            reply_to=event.id
        )
    else:
        await client.send_message(event.chat_id, "ᴋișiʏi ɢʀᴜᴘᴛᴀɴ ᴀᴛᴍᴀᴋ içiɴ ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ!", reply_to=event.id)

# 😘 /kiss (sadece grupta)
@client.on(events.NewMessage(pattern="^/kiss$"))
async def kiss(event):
    if not event.is_group:
        return
    if event.is_reply:
        reply = await event.get_reply_message()
        await client.send_message(
            event.chat_id,
            f"{event.sender.first_name} {reply.sender.first_name}’i öᴘᴛü!",
            reply_to=event.id
        )
    else:
        await client.send_message(event.chat_id, "ʙiʀisiɴi ōᴘᴍᴇᴋ içiɴ ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ!!", reply_to=event.id)

# 🤗 /saril (sadece grupta)
@client.on(events.NewMessage(pattern="^/saril$"))
async def saril(event):
    if not event.is_group:
        return
    if event.is_reply:
        reply = await event.get_reply_message()
        await client.send_message(
            event.chat_id,
            f"{event.sender.first_name} {reply.sender.first_name}’ᴇ sᴀʀɪʟᴅɪ!",
            reply_to=event.id
        )
    else:
        await client.send_message(event.chat_id, "ʙiʀisiɴᴇ sᴀʀɪʟᴍᴀᴋ içiɴ ᴍᴇsᴀᴊɪɴɪ ʏᴀɴɪᴛʟᴀ!!", reply_to=event.id)

# /destek komutu
@client.on(events.NewMessage(pattern="^/destek(?: (.+))?"))
async def destek(event):
    destek_mesaj = event.pattern_match.group(1)

    # Mesaj yoksa kullanım göster
    if not destek_mesaj:
        await event.respond("❌ ᴋᴜʟʟᴀɴɪᴍ: `/destek <mesajınız>`", reply_to=event.id)
        return

    # Mesaj 5 harften kısa ise uyar
    if len(destek_mesaj.strip()) < 5:
        await event.respond("❌ ɢᴇçᴇʀsiᴢ ᴍᴇsᴀᴊ, ᴇɴ ᴀᴢ 5 ᴋᴀʀᴀᴋᴛᴇʀ ᴏʟᴍᴀʟɪᴅɪʀ ᴍᴇsᴀᴊ!", reply_to=event.id)
        return

    # Onay butonları
    buttons = [
        [Button.inline("✅ ᴏɴᴀʏʟᴀ", b"onay"), Button.inline("❌ iᴘᴛᴀʟ", b"iptal")]
    ]

    msg = await event.respond(
        f"📨 ᴅᴇsᴛᴇᴋ ᴍᴇsᴀᴊɪɴɪᴢɪ ᴇᴋiʙᴇ iʟᴇᴛᴍᴇᴋ isᴛᴇᴅiɢiɴiᴢᴇ ᴇᴍiɴ ᴍisiɴiᴢ?\n\nᴍᴇsᴀᴊ: {destek_mesaj}",
        buttons=buttons,
        reply_to=event.id
    )

    # Callback handler
    @client.on(events.CallbackQuery)
    async def callback(event_cb):
        # Sadece destek mesajını açan kullanıcı basabilir
        if event_cb.sender_id != event.sender_id:
            await event_cb.answer("ʙᴜ ʏᴀʀᴅɪᴍ ᴋᴏᴍᴜᴛᴜɴᴜ siᴢ ᴀçᴍᴀᴅɪɴɪᴢ!", alert=True)
            return

        if event_cb.data == b"onay":
            # Grup adı
            grup_adi = event.chat.title if event.chat else "DM"

            # Kullanıcı username
            username = event.sender.username if event.sender.username else "Yok"

            # Mesajı admin ID'ye gönder
            destek_metni = f"""📩 __ʏᴇɴi ᴛiᴄᴋᴇᴛ:__

**ɢʀᴜᴘ ᴀᴅɪ:** {grup_adi}

**ᴜsᴇʀ ɴᴀᴍᴇ:** {username}
**ᴜsᴇʀ ɪᴅ:** {event.sender_id}
**iʟᴇᴛi:** {destek_mesaj}"""
            
            await client.send_message(ADMIN_ID, destek_metni)
            await event_cb.edit(f"🟢 ᴅᴇsᴛᴇᴋ ᴍᴇsᴀᴊɪɴɪᴢ ᴇᴋiʙiᴍiᴢᴇ iʟᴇᴛiʟᴅi, ᴇɴ ᴋɪsᴀ süʀᴇᴅᴇ ʏᴀʀᴅɪᴍ, ᴠᴇʏᴀ ᴅöɴüș ʏᴀᴘɪʟɪᴄᴀᴋᴛɪʀ.")

        elif event_cb.data == b"iptal":
            await event_cb.edit(f"🔴 ᴛiᴄᴋᴇᴛ ᴀçɪʟᴍᴀᴅɪ, iʏi sᴏʜʙᴇᴛʟᴇʀ...")



# /id komutu: Kullanıcının ID'sini gösterir
@client.on(events.NewMessage(pattern="^/id$"))
async def show_id(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await client.get_entity(reply.sender_id)
        await client.send_message(event.chat_id, f"👤 **{user.first_name}** 🆔 ID: `{user.id}`", reply_to=event.id)
    else:
        await client.send_message(event.chat_id, f"🧑 Senin ID: `{event.sender_id}`", reply_to=event.id)


# /info komutu: Kullanıcının bilgilerini gösterir
@client.on(events.NewMessage(pattern="^/info$"))
async def show_info(event):
    if event.is_reply:
        reply = await event.get_reply_message()
        user = await client.get_entity(reply.sender_id)
    else:
        user = await client.get_entity(event.sender_id)

    info_text = (
        f"**ᴜsᴇʀ iɴғᴏ:**\n\n"
        f"ᴜsᴇʀ ғiʀsᴛɴᴀᴍᴇ: {user.first_name or 'Yok'}\n"
        f"ᴜsᴇʀɴᴀᴍᴇ: @{user.username or 'Yok'}\n"
        f"ɪᴅ: {user.id}\n"
        f"ʙiʏᴏɢʀᴀғɪ: {getattr(user, 'about', 'Yok')}\n"
    )

    await client.send_message(event.chat_id, info_text, reply_to=event.id)

print("[INFO] - ᴀʀᴛᴢ ᴘʀᴏᴊᴇᴄᴛ, ᴀᴋᴛiғ 🟢")
client.run_until_disconnected()
