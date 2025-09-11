from telethon import TelegramClient, events
import platform, time, random, asyncio, requests

# --- API Ayarları ---
API_ID = 21883581
API_HASH = "c3b4ba58d5dada9bc8ce6c66e09f3f12"
SESSION = "session_userbot"

client = TelegramClient(SESSION, API_ID, API_HASH)
START_TIME = time.time()

# --- YARDIMCI FONKSİYON ---
def uptime_text():
    uptime = int(time.time() - START_TIME)
    h, m = divmod(uptime // 60, 60)
    s = uptime % 60
    return f"{h} saat {m} dk {s} sn"

# --- KOMUTLAR ---
@client.on(events.NewMessage(pattern=r'^\.artz$', incoming=True))
async def bot_info(event):
    await event.reply(
        "🤖 **Artz Userbot**\n"
        "👤 Sahibi: [Artz](https://t.me/artzfounder)\n"
        "🛠 Versiyon: 1.0\n"
        "💡 Komutlar: .alive, .help, .duyuru, .zarar, .id, .info, .say, .flip, .roll, .sticker, .quote, .weather, .remind, .calc"
    )

@client.on(events.NewMessage(pattern=r'^\.alive$', incoming=True))
async def alive(event):
    await event.reply(
        f"✅ Bot aktif!\n⏱ Uptime: {uptime_text()}\n"
        f"💻 Sistem: {platform.system()} {platform.release()}\n"
        f"🐍 Python: {platform.python_version()}"
    )

@client.on(events.NewMessage(pattern=r'^\.help$', incoming=True))
async def help_cmd(event):
    await event.reply(
        "📜 **Komutlar:**\n"
        "🤖 .artz → Bot bilgisi\n"
        "⏱ .alive → Bot aktif mi?\n"
        "🆔 .id → Kullanıcı ID\n"
        "ℹ️ .info → Kullanıcı bilgisi\n"
        "📢 .duyuru <mesaj> → Duyuru gönder\n"
        "💥 .zarar → Örnek komut\n"
        "🗣 .say <mesaj> → Bot mesajını tekrar eder\n"
        "🎲 .roll → 1-100 arası zar atar\n"
        "🔄 .flip → Yazı tura atar\n"
        "🖼 .sticker → Örnek sticker gönderir\n"
        "💬 .quote → Rastgele alıntı\n"
        "🌦 .weather <şehir> → Hava durumu\n"
        "⏰ .remind <süre> <mesaj> → Hatırlatma kurar\n"
        "🧮 .calc <işlem> → Basit hesaplama"
    )

@client.on(events.NewMessage(pattern=r'^\.id$', incoming=True))
async def id_cmd(event):
    sender = await event.get_sender()
    await event.reply(f"🆔 Senin ID: {sender.id}")

@client.on(events.NewMessage(pattern=r'^\.info$', incoming=True))
async def info_cmd(event):
    sender = await event.get_sender()
    await event.reply(
        f"👤 Ad: {sender.first_name}\n"
        f"🆔 ID: {sender.id}\n"
        f"💬 Username: @{sender.username if sender.username else 'Yok'}"
    )

# --- YENİ KOMUTLAR ---
@client.on(events.NewMessage(pattern=r'^\.say (.+)$', incoming=True))
async def say_cmd(event):
    await event.reply(event.pattern_match.group(1))

@client.on(events.NewMessage(pattern=r'^\.roll$', incoming=True))
async def roll_cmd(event):
    await event.reply(f"🎲 Zar sonucu: {random.randint(1,100)}")

@client.on(events.NewMessage(pattern=r'^\.flip$', incoming=True))
async def flip_cmd(event):
    await event.reply("🔄 " + random.choice(["Yazı", "Tura"]))

@client.on(events.NewMessage(pattern=r'^\.quote$', incoming=True))
async def quote_cmd(event):
    quotes = [
        "💬 Hayat kısa, tadını çıkar.",
        "💬 Başarı azimli olanların hakkıdır.",
        "💬 Bugün, geleceğin başlangıcıdır.",
        "💬 Başarı küçük adımlarla gelir.",
        "💬 Cesur ol, risk al!",
        "💬 Sabır her zaman kazandırır.",
        "💬 Öğrenmek için asla geç değildir.",
        "💬 Hayallerinin peşinden git.",
        "💬 Her gün yeni bir fırsattır.",
        "💬 Olumsuzluklara takılma."
    ]
    await event.reply(random.choice(quotes))

@client.on(events.NewMessage(pattern=r'^\.zarar$', incoming=True))
async def zarar_cmd(event):
    await event.reply("💥 Bu bir örnek zarardır, sadece test amaçlı!")

@client.on(events.NewMessage(pattern=r'^\.duyuru (.+)$', incoming=True))
async def duyuru_cmd(event):
    await event.reply(f"📢 Duyuru: {event.pattern_match.group(1)}")

@client.on(events.NewMessage(pattern=r'^\.sticker$', incoming=True))
async def sticker_cmd(event):
    await event.reply("🖼 [Sticker placeholder]")  # Sticker URL veya file eklenebilir

@client.on(events.NewMessage(pattern=r'^\.weather (.+)$', incoming=True))
async def weather_cmd(event):
    city = event.pattern_match.group(1)
    await event.reply(f"🌦 Hava durumu bilgisi: {city} (örnek veri)")

@client.on(events.NewMessage(pattern=r'^\.remind (\d+) (.+)$', incoming=True))
async def remind_cmd(event):
    seconds = int(event.pattern_match.group(1))
    msg = event.pattern_match.group(2)
    await event.reply(f"⏰ Hatırlatma {seconds} saniye sonra ayarlandı!")
    await asyncio.sleep(seconds)
    await event.reply(f"⏰ Hatırlatma: {msg}")

@client.on(events.NewMessage(pattern=r'^\.calc (.+)$', incoming=True))
async def calc_cmd(event):
    expr = event.pattern_match.group(1)
    try:
        result = eval(expr)
        await event.reply(f"🧮 Sonuç: {result}")
    except Exception:
        await event.reply("⚠️ Hatalı işlem!")

# --- GİZLİ SÜRELİ MESAJ LOG ---
@client.on(events.NewMessage(incoming=True))
async def secret_media(event):
    if event.is_private and event.message.ttl_period and event.message.media:
        await client.send_file("me", event.message.media)

if __name__ == "__main__":
    print("[INFO] Artz Userbot başlatılıyor...")
    client.start()  # Oturum aç
    me = client.loop.run_until_complete(client.get_me())  # Kendi bilgilerini al
    # Kayıtlı Mesajlar'a bilgi gönder
    client.loop.run_until_complete(client.send_message(
        "me",
        f"✅ Artz Userbot aktif!\n👤 Kullanıcı: {me.first_name}\n⏱ Uptime: 0 sn\n🤖 Sahibi: [Artz](https://t.me/artzfounder)"
    ))
    print(f"[INFO] {me.first_name} ile giriş yapıldı, bot aktif!")
    client.run_until_disconnected()  # Botu sürekli çalıştır
