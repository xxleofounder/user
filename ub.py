from telethon import TelegramClient, events, Button
import platform, psutil, time, random
from datetime import datetime

# -----------------------------
# TELEGRAM API BİLGİLERİ
# -----------------------------
API_ID = 21883581          # kendi API_ID
API_HASH = "c3b4ba58d5dada9bc8ce6c66e09f3f12"  # kendi API_HASH
ALLOWED_USER_ID = 8276543841  # kendi user id

client = TelegramClient("artz", API_ID, API_HASH)

start_time = time.time()  # uptime için

# -----------------------------
# KOMUTLAR
# -----------------------------
@client.on(events.NewMessage(pattern=r"^\.alive$"))
async def alive(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    await event.edit("✅ Artz Userbot aktif ve çalışıyor!")

@client.on(events.NewMessage(pattern=r"^\.ping$"))
async def ping(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    start = time.time()
    await event.edit("🏓 Pong!")
    end = time.time()
    await event.edit(f"🏓 Pong! `{round((end-start)*1000)} ms`")

@client.on(events.NewMessage(pattern=r"^\.id$"))
async def user_id(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        user = await event.get_reply_message()
        await event.edit(f"👤 ID: `{user.sender_id}`")
    else:
        await event.edit(f"👤 Senin ID: `{ALLOWED_USER_ID}`")

@client.on(events.NewMessage(pattern=r"^\.info$"))
async def user_info(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        user = await event.get_reply_message().sender
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

@client.on(events.NewMessage(pattern=r"^\.help$"))
async def help_cmd(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    msg = "**ARTZ USERBOT KOMUTLARI**\n\n" \
          ".alive\n.ping\n.id\n.info\n.sysinfo\n.time\n.flip\n.echo <yazi>\n.del\n.chatinfo\n.owner\n.server\n.uptime\n.bio\n.link\n.stats"
    await event.edit(msg, buttons=[Button.url("Owner", "https://t.me/artzfounder")])

@client.on(events.NewMessage(pattern=r"^\.sysinfo$"))
async def sys_info(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    cpu = psutil.cpu_count(logical=True)
    ram = round(psutil.virtual_memory().total / (1024**3), 2)
    await event.edit(f"💻 Sistem: {platform.system()} {platform.release()}\n🖥️ CPU: {cpu} Core\n🔋 RAM: {ram} GB")

@client.on(events.NewMessage(pattern=r"^\.time$"))
async def current_time(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await event.edit(f"⏰ Şu anki zaman: {now}")

@client.on(events.NewMessage(pattern=r"^\.flip$"))
async def flip(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    choice = random.choice(["Yazı", "Tura"])
    await event.edit(f"🎲 Sonuç: {choice}")

@client.on(events.NewMessage(pattern=r"^\.echo (.+)"))
async def echo(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    text = event.pattern_match.group(1)
    await event.edit(text)

@client.on(events.NewMessage(pattern=r"^\.del$"))
async def delete_msg(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    await event.delete()

@client.on(events.NewMessage(pattern=r"^\.chatinfo$"))
async def chat_info(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    chat = await event.get_chat()
    info = f"💬 Chat Name: {getattr(chat, 'title', 'Private Chat')}\n🆔 Chat ID: {chat.id}"
    await event.edit(info)

@client.on(events.NewMessage(pattern=r"^\.owner$"))
async def owner(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    await event.edit("💠 Owner: t.me/artzfounder")

@client.on(events.NewMessage(pattern=r"^\.server$"))
async def server_info(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    ip = "127.0.0.1"  # VPS ip tespiti için eklenebilir
    await event.edit(f"💻 VPS IP: {ip}\nOS: {platform.system()} {platform.release()}")

@client.on(events.NewMessage(pattern=r"^\.uptime$"))
async def uptime(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    up = time.time() - start_time
    await event.edit(f"⏱️ Uptime: {int(up)} saniye")

@client.on(events.NewMessage(pattern=r"^\.bio$"))
async def bio(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    if event.is_reply:
        user = await event.get_reply_message().sender
        await event.edit(f"📝 Bio: {user.bot or 'Yok'}")
    else:
        me = await client.get_me()
        await event.edit(f"📝 Bio: {me.bot or 'Yok'}")

@client.on(events.NewMessage(pattern=r"^\.link$"))
async def chat_link(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    chat = await event.get_chat()
    if hasattr(chat, 'username') and chat.username:
        await event.edit(f"🔗 t.me/{chat.username}")
    else:
        await event.edit("🔗 Bu chat linke sahip değil.")

@client.on(events.NewMessage(pattern=r"^\.stats$"))
async def chat_stats(event):
    if event.sender_id != ALLOWED_USER_ID:
        return
    chat = await event.get_chat()
    msg_count = "Bilinmiyor"  # İleri düzey API ile alınabilir
    await event.edit(f"📊 Chat Stats:\nID: {chat.id}\nMesaj sayısı: {msg_count}")


# -----------------------------
# BOT BAŞLATMA
# -----------------------------
client.start()
me = client.loop.run_until_complete(client.get_me())
print(f"[INFO] {me.first_name} ile giriş yapıldı, bot aktif!")

client.run_until_disconnected()
