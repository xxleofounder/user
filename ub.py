# userbot.py
import os
import platform
import time
from telethon import TelegramClient, events


API_ID = 21883581
API_HASH = "c3b4ba58d5dada9bc8ce6c66e09f3f12" 
SESSION = "session_"
OWNER_ID = None

client = TelegramClient(SESSION, API_ID, API_HASH)
START_TIME = time.time()

def allowed_sender(sender_id):
    if not OWNER_ID:
        return True
    return str(sender_id) == str(OWNER_ID)

# .artz ping
@client.on(events.NewMessage(pattern=r'^\.artz ping$', incoming=True))
async def handler_ping(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    msg = await event.reply("🏓.")
    await client.sleep(0.4)
    await msg.edit("🏓 Po..")
    await client.sleep(0.4)
    await msg.edit("🏓 Pong!")
    latency = round((time.time() - event.message.date.timestamp()) * 1000, 2)
    await client.sleep(0.4)
    await msg.edit(f"🏓 Pong!\n⚡️ Gecikme: `{latency} ms`")
    print(f"[PING] {sender.first_name} ({sender.id}) ping yaptı: {latency} ms")

# .artz alive
@client.on(events.NewMessage(pattern=r'^\.artz alive$', incoming=True))
async def handler_alive(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    me = await client.get_me()
    uptime = int(time.time() - START_TIME)
    h, m = divmod(uptime // 60, 60)
    s = uptime % 60
    await event.reply(
        f"✨ **Bot Durumu** ✨\n\n"
        f"👤 Kullanıcı: `{me.first_name}`\n"
        f"🆔 ID: `{me.id}`\n"
        f"⚡️ Uptime: `{h} saat {m} dk {s} sn`\n"
        f"💻 Platform: `{platform.system()} {platform.release()}`\n"
        f"🐍 Python: `{platform.python_version()}`\n\n"
        f"✅ **Bot aktif ve çalışıyor!**"
    )
    print(f"[ALIVE] {sender.first_name} botun durumunu sorguladı.")

# .artz id
@client.on(events.NewMessage(pattern=r'^\.artz id$', incoming=True))
async def handler_id(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    await event.reply(f"🆔 Senin Telegram ID'in: `{sender.id}`")
    print(f"[ID] {sender.first_name} ID sorguladı: {sender.id}")

# .artz info
@client.on(events.NewMessage(pattern=r'^\.artz info$', incoming=True))
async def handler_info(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    me = await client.get_me()
    await event.reply(
        f"ℹ️ **Bilgilerim**:\n\n"
        f"👤 Ad: {me.first_name}\n"
        f"🆔 ID: `{me.id}`\n"
        f"💬 Username: @{me.username if me.username else 'Yok'}"
    )
    print(f"[INFO] {sender.first_name} bot bilgilerini sorguladı.")

# .artz sys
@client.on(events.NewMessage(pattern=r'^\.artz sys$', incoming=True))
async def handler_sys(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    uptime = int(time.time() - START_TIME)
    h, m = divmod(uptime // 60, 60)
    s = uptime % 60
    await event.reply(
        f"🖥 **Sistem Bilgisi**\n\n"
        f"⚡️ Uptime: `{h} saat {m} dk {s} sn`\n"
        f"💻 İşletim Sistemi: {platform.system()} {platform.release()}\n"
        f"🐍 Python: `{platform.python_version()}`"
    )
    print(f"[SYS] {sender.first_name} sistem bilgisi sorguladı.")

# .artz help
@client.on(events.NewMessage(pattern=r'^\.artz help$', incoming=True))
async def handler_help(event):
    sender = await event.get_sender()
    if not allowed_sender(sender.id):
        return
    await event.reply(
        "📜 **Komutlar:**\n\n"
        "➡️ `.artz alive` → Bot aktif mi?\n"
        "➡️ `.artz ping` → Ping testi (animasyonlu)\n"
        "➡️ `.artz id` → Kullanıcı ID öğren\n"
        "➡️ `.artz info` → Hesap bilgilerini göster\n"
        "➡️ `.artz sys` → Sistem bilgisi\n"
        "➡️ `.artz help` → Bu yardım menüsü\n"
    )
    print(f"[HELP] {sender.first_name} yardım menüsünü görüntüledi.")

# Ana başlatma
if __name__ == "__main__":
    print("[INFO] Bot başlatılıyor...")
    client.start()
    me = client.loop.run_until_complete(client.get_me())
    print(f"[INFO] Bot çalışıyor: {me.first_name} ({me.id})")
    print("[INFO] Artz Userbot aktif! Ctrl+C ile kapatabilirsiniz.")
    client.run_until_disconnected()
