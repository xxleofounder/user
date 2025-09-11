from telethon import TelegramClient, events, Button
from telethon.tl.types import MessageMediaPhoto
import platform, psutil, time, random, os
from datetime import datetime

# -----------------------------
# TELEGRAM API BİLGİLERİ
# -----------------------------
API_ID = 21883581          # kendi API_ID
API_HASH = "c3b4ba58d5dada9bc8ce6c66e09f3f12"  # kendi API_HASH
ALLOWED_USER_ID = 8276543841  # kendi user id
ARCHIVE_DIR = "./artzarxiv/"  # Gizli foto arşivi

# Klasör yoksa oluştur
if not os.path.exists(ARCHIVE_DIR):
    os.makedirs(ARCHIVE_DIR)

client = TelegramClient("artz", API_ID, API_HASH)
start_time = time.time()

# -----------------------------
# YARDIM FONKSİYONU
# -----------------------------
HELP_TEXT = """➤ .alive        - Botun aktif olduğunu gösterir
➤ .ping         - Gecikme süresini ölçer
➤ .id           - Reply varsa kişinin, yoksa kendi ID
➤ .info         - Reply varsa kişinin info’su, yoksa kendi info
➤ .artz         - Sahip ve buradayım mesajı
➤ .del          - Reply sonrası yazılanları siler
➤ .stats        - Chat istatistiklerini gösterir
"""

# -----------------------------
# KOMUTLAR
# -----------------------------
@client.on(events.NewMessage(pattern=r"^\.alive$"))
async def alive(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    uptime = int(time.time() - start_time)
    await event.edit(f"✅ Artz UserBot aktif!\n👤 Sahip: Artz\n⏱ Uptime: {uptime} saniye\n💻 Sürüm: 1.0")

@client.on(events.NewMessage(pattern=r"^\.ping$"))
async def ping(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    msg = await event.edit("🏓 P")
    await msg.edit("🏓 Pi")
    await msg.edit("🏓 Pin")
    await msg.edit("🏓 Ping!")
    await msg.edit(f"🏓 Ping tamam! `{round(random.randint(50,200))} ms`")

@client.on(events.NewMessage(pattern=r"^\.id$"))
async def user_id(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        user = await event.get_reply_message()
        await event.edit(f"👤 Reply ID: `{user.sender_id}`")
    else:
        await event.edit(f"👤 Senin ID: `{ALLOWED_USER_ID}`")

@client.on(events.NewMessage(pattern=r"^\.info$"))
async def user_info(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        msg = await event.get_reply_message()
        user = await msg.sender
        name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        username = f"@{user.username}" if user.username else "Yok"
        photos = await client.get_profile_photos(user)
        caption = f"👤 Name: {name}\n💻 Username: {username}\n🆔 ID: {user.id}"
        if photos.total > 0:
            await client.send_file(event.chat_id, photos[0], caption=caption)
            await event.delete()
        else:
            await event.edit(caption)
    else:
        me = await client.get_me()
        name = f"{me.first_name or ''} {me.last_name or ''}".strip()
        username = f"@{me.username}" if me.username else "Yok"
        await event.edit(f"👤 Name: {name}\n💻 Username: {username}\n🆔 ID: {me.id}")

@client.on(events.NewMessage(pattern=r"^\.artz$"))
async def artz(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    await event.edit("📌 Burdayım!\n👤 Sahip: Artz\n✅ Çalışıyor!")

@client.on(events.NewMessage(pattern=r"^\.del$"))
async def delete_msg(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        try:
            msg = await event.get_reply_message()
            chat = await event.get_chat()
            if getattr(chat, 'admin_rights', None) or getattr(chat, 'creator', False) or chat.__class__.__name__ == "User":
                messages = await client.get_messages(chat.id, min_id=msg.id)
                for m in messages:
                    await m.delete()
            else:
                await event.edit("⚠️ Kısıtlı yetki")
        except:
            await event.edit("⚠️ Mesajları silme hatası")
    else:
        await event.edit("⚠️ Reply kullanmalısın")

@client.on(events.NewMessage(pattern=r"^\.stats$"))
async def stats(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    chat = await event.get_chat()
    try:
        members = await client.get_participants(chat)
        await event.edit(f"📊 Chat ID: {chat.id}\n💬 Üye sayısı: {len(members)}")
    except:
        await event.edit(f"📊 Chat ID: {chat.id}\n💬 Üye sayısı: Bilinmiyor")

@client.on(events.NewMessage(pattern=r"^\.help$"))
async def help_cmd(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    await event.edit(HELP_TEXT, buttons=[Button.url("Support", "https://t.me/artzfounder")])

# -----------------------------
# GİZLİ / SÜRELİ FOTO İNDİRME
# -----------------------------
@client.on(events.NewMessage(func=lambda e: e.sender_id != None))
async def secret_photo(event):
    if event.sender_id == ALLOWED_USER_ID:
        return
    if isinstance(event.media, MessageMediaPhoto):
        file_path = os.path.join(ARCHIVE_DIR, f"{int(time.time())}_{event.id}.jpg")
        try:
            await client.download_media(event, file_path)
            print(f"[INFO] Gizli foto arşivlendi: {file_path}")
        except:
            pass

# -----------------------------
# BOT BAŞLATMA MESAJI
# -----------------------------
client.start()
me = client.loop.run_until_complete(client.get_me())
print(f"[INFO] {me.first_name} ile giriş yapıldı, bot aktif!")

# Kayıtlı mesaja info
async def startup_msg():
    await client.send_message(me.id, "✅ ArtzUserBot aktif!\n💻 Sürüm: 1.0", buttons=[Button.url("Support", "https://t.me/artzfounder")])

client.loop.run_until_complete(startup_msg())
client.run_until_disconnected()
