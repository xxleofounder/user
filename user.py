import os
import asyncio
import random
import platform
import time
import psutil
from datetime import datetime
from telethon import TelegramClient, events
from dotenv import load_dotenv
import pyfiglet

load_dotenv()

API_ID = int(os.getenv("21883581"))
API_HASH = os.getenv("c3b4ba58d5dada9bc8ce6c66e09f3f12")
SESSION = os.getenv("SESSION_NAME", "session")

client = TelegramClient(SESSION, API_ID, API_HASH)
START_TIME = time.time()

# Tagall kontrol flag
tagall_running = False


def format_uptime(seconds: int):
    h, m = divmod(seconds // 60, 60)
    s = seconds % 60
    return f"{h} saat {m} dk {s} sn"


# ================== TEMEL KOMUTLAR ==================

@client.on(events.NewMessage(pattern=r'^\.artz$', incoming=True))
async def handler_cilveli(event):
    user = await event.get_sender()
    firstname = user.first_name

    messages = [
        f"💁‍♀️ Buradayım, {firstname}! ArtzUserbot v1.0. Sahibim [t.me/artzfounder] Size hizmet vermek için geliştirildi 😉",
        f"🌟 Selam {firstname}! Ben ArtzUserbot v1.0, sahibim [t.me/artzfounder] beni gönderdi 😏",
        f"😎 Merhaba {firstname}! ArtzUserbot v1.0 burada. Eğlence başlasın! ✨",
        f"✨ {firstname}, ArtzUserbot v1.0 sizi selamlıyor! Sahibim [t.me/artzfounder] her zaman yanınızda 😏",
        f"💃 Hey {firstname}! ArtzUserbot v1.0 hazır, sahibim [t.me/artzfounder] beni çağırdı 💫"
    ]

    await event.reply(random.choice(messages))

@client.on(events.NewMessage(pattern=r'^\.artz ping$', incoming=True))
async def handler_ping(event):
    msg = await event.reply("🏓.")
    for step in ["🏓 Po..", "🏓 Pong!"]:
        await asyncio.sleep(0.4)
        await msg.edit(step)
    latency = round((time.time() - event.message.date.timestamp()) * 1000, 2)
    await asyncio.sleep(0.4)
    await msg.edit(f"🏓 Pong!\n⚡️ Gecikme: `{latency} ms`")


@client.on(events.NewMessage(pattern=r'^\.artz alive$', incoming=True))
async def handler_alive(event):
    me = await client.get_me()
    uptime = int(time.time() - START_TIME)
    await event.reply(
        f"✨ **Bot Durumu** ✨\n\n"
        f"👤 Kullanıcı: `{me.first_name}`\n"
        f"🆔 ID: `{me.id}`\n"
        f"⚡️ Uptime: `{format_uptime(uptime)}`\n"
        f"💻 Platform: `{platform.system()} {platform.release()}`\n"
        f"🐍 Python: `{platform.python_version()}`\n\n"
        f"✅ **Bot aktif ve çalışıyor!**"
    )


@client.on(events.NewMessage(pattern=r'^\.artz id$', incoming=True))
async def handler_id(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()
    else:
        user = await event.get_sender()
    await event.reply(f"🆔 Kullanıcı: `{user.first_name}`\nID: `{user.id}`")


@client.on(events.NewMessage(pattern=r'^\.artz info$', incoming=True))
async def handler_info(event):
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        user = await reply_msg.get_sender()
    else:
        user = await client.get_me()
    await event.reply(
        f"ℹ️ **Bilgiler**:\n\n"
        f"👤 Ad: {user.first_name}\n"
        f"🆔 ID: `{user.id}`\n"
        f"💬 Username: @{user.username if user.username else 'Yok'}\n"
    )


@client.on(events.NewMessage(pattern=r'^\.artz sys$', incoming=True))
async def handler_sys(event):
    uptime = int(time.time() - START_TIME)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    await event.reply(
        f"🖥 **Sistem Bilgisi**\n\n"
        f"⚡️ Uptime: `{format_uptime(uptime)}`\n"
        f"💻 İşletim Sistemi: {platform.system()} {platform.release()}\n"
        f"🐍 Python: {platform.python_version()}\n"
        f"🧠 RAM Kullanımı: %{mem}\n"
        f"🌀 CPU Kullanımı: %{cpu}"
    )


@client.on(events.NewMessage(pattern=r'^\.artz time$', incoming=True))
async def handler_time(event):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    await event.reply(f"⏰ Şu anki tarih & saat: `{now}`")


@client.on(events.NewMessage(pattern=r'^\.artz count$', incoming=True))
async def handler_count(event):
    if not (await event.get_input_chat()).is_group:
        await event.reply("❌ Bu komut sadece gruplarda çalışır.")
        return
    participants = await client.get_participants(event.chat_id)
    await event.reply(f"👥 Bu grupta **{len(participants)}** üye var.")


# ================== TAGALL / TAGDUR ==================

@client.on(events.NewMessage(pattern=r'^\.artz tagall(?:\s+(.*))?$', incoming=True))
async def handler_tagall(event):
    global tagall_running
    if not (await event.get_input_chat()).is_group:
        await event.reply("❌ Bu komut sadece gruplarda çalışır.")
        return

    text = event.pattern_match.group(1)
    if not text:
        await event.reply("ℹ️ Kullanım: `.artz tagall <mesaj>`\n\n"
                          "Gruptaki herkesi 5 saniye aralıklarla etiketler.")
        return

    tagall_running = True
    users = await client.get_participants(event.chat_id)
    batch = []
    count = 0

    for user in users:
        if not tagall_running:
            await event.reply("⏹ Etiketleme durduruldu.")
            return

        batch.append(f"[{user.first_name}](tg://user?id={user.id})")
        if len(batch) == 10:
            await event.reply(f"📢 {text}\n\n{' '.join(batch)}")
            batch = []
            count += 10
            await asyncio.sleep(5)

    if batch and tagall_running:
        await event.reply(f"📢 {text}\n\n{' '.join(batch)}")
        count += len(batch)

    await event.reply(f"✅ Toplam {count} kişi etiketlendi.")


@client.on(events.NewMessage(pattern=r'^\.artz tagdur$', incoming=True))
async def handler_tagdur(event):
    global tagall_running
    tagall_running = False
    await event.reply("⏹ Etiketleme işlemi durduruldu.")


# ================== EĞLENCELİ KOMUTLAR ==================

@client.on(events.NewMessage(pattern=r'^\.artz zar$', incoming=True))
async def handler_zar(event):
    await event.reply(f"🎲 Zar sonucu: {random.randint(1,6)}")


@client.on(events.NewMessage(pattern=r'^\.artz yazitura$', incoming=True))
async def handler_yazitura(event):
    await event.reply(f"🪙 Sonuç: {random.choice(['Yazı', 'Tura'])}")


@client.on(events.NewMessage(pattern=r'^\.artz sayı (\d+)$', incoming=True))
async def handler_sayi(event):
    max_num = int(event.pattern_match.group(1))
    await event.reply(f"🔢 Rastgele sayı: {random.randint(1, max_num)}")


@client.on(events.NewMessage(pattern=r'^\.artz şaka$', incoming=True))
async def handler_saka(event):
    jokes = [
        "Adamın biri güneşte yanmış, ayda da düz!",
        "Matematik öğretmeni denize düşerse ne olur? Cevap: Cebirlenir!",
        "Temel’e sormuşlar: En hızlı hayvan hangisi? İnek, çünkü sütü yoğurt oluyor 😅"
    ]
    await event.reply(f"😂 {random.choice(jokes)}")


@client.on(events.NewMessage(pattern=r'^\.artz bilgi$', incoming=True))
async def handler_bilgi(event):
    facts = [
        "🐝 Arılar insanların yüzlerini tanıyabilir.",
        "🌍 Dünya yüzeyinin %70’i okyanuslarla kaplıdır.",
        "🧠 İnsan beyninde yaklaşık 86 milyar nöron vardır."
    ]
    await event.reply(f"ℹ️ Bilgi: {random.choice(facts)}")


@client.on(events.NewMessage(pattern=r'^\.artz atasözü$', incoming=True))
async def handler_atasozu(event):
    proverbs = [
        "Taş yerinde ağırdır.",
        "Ayağını yorganına göre uzat.",
        "Üzüm üzüme baka baka kararır."
    ]
    await event.reply(f"📜 Atasözü: {random.choice(proverbs)}")


@client.on(events.NewMessage(pattern=r'^\.artz espri$', incoming=True))
async def handler_espri(event):
    espriler = [
        "Telefonun şarjı neden bitmiş? Çünkü çok konuşmuş! 📱",
        "Ben kahve içince neden uyanmıyorum? Çünkü uyurken içiyorum! 😴",
    ]
    await event.reply(f"🤣 {random.choice(espriler)}")


@client.on(events.NewMessage(pattern=r'^\.artz quote$', incoming=True))
async def handler_quote(event):
    quotes = [
        "“Ya olduğun gibi görün, ya göründüğün gibi ol.” – Mevlana",
        "“Bilgi güçtür.” – Francis Bacon",
        "“Düşünmek kolaydır, yapmak zordur.” – Goethe"
    ]
    await event.reply(f"💬 {random.choice(quotes)}")


@client.on(events.NewMessage(pattern=r'^\.artz ascii (.+)$', incoming=True))
async def handler_ascii(event):
    text = event.pattern_match.group(1)
    ascii_art = pyfiglet.figlet_format(text)
    await event.reply(f"```\n{ascii_art}\n```")


@client.on(events.NewMessage(pattern=r'^\.artz oyun$', incoming=True))
async def handler_oyun(event):
    choices = ["✊ Taş", "✋ Kağıt", "✌️ Makas"]
    bot_choice = random.choice(choices)
    await event.reply(f"🎮 Taş-Kağıt-Makas oynuyorum...\nBenim seçimim: {bot_choice}")


# ================== GİZLİ MEDYA ARŞİVLEME ==================

@client.on(events.NewMessage(incoming=True))
async def secret_media_handler(event):
    if event.photo or event.video:
        if event.message.ttl_seconds:  # self-destruct medya
            await client.send_message("me", f"📸 Gizli medya {event.sender_id} kullanıcısından arşivlendi:")
            await client.forward_messages("me", event.message)


# ================== HELP MENÜ ==================

@client.on(events.NewMessage(pattern=r'^\.artz help$', incoming=True))
async def handler_help(event):
    await event.reply(
        "📜 **Komutlar:**\n\n"
        "➡️ `.artz alive` → Bot aktif mi?\n"
        "➡️ `.artz ping` → Ping testi\n"
        "➡️ `.artz id` → Kullanıcı ID (yanıtla çalışır)\n"
        "➡️ `.artz info` → Kullanıcı bilgisi (yanıtla çalışır)\n"
        "➡️ `.artz sys` → Sistem bilgisi\n"
        "➡️ `.artz time` → Anlık tarih & saat\n"
        "➡️ `.artz count` → Grup üye sayısı\n"
        "➡️ `.artz tagall <mesaj>` → 10 kişilik etiketleme (5sn aralıklı)\n"
        "➡️ `.artz tagdur` → Etiketlemeyi durdur\n"
        "➡️ `.artz zar` → Zar atar\n"
        "➡️ `.artz yazitura` → Yazı-tura atar\n"
        "➡️ `.artz sayı <max>` → Rastgele sayı üretir\n"
        "➡️ `.artz şaka` → Rastgele şaka\n"
        "➡️ `.artz bilgi` → İlginç bilgi\n"
        "➡️ `.artz atasözü` → Atasözü\n"
        "➡️ `.artz espri` → Espri yapar\n"
        "➡️ `.artz quote` → Alıntı söz\n"
        "➡️ `.artz ascii <metin>` → ASCII yazı\n"
        "➡️ `.artz oyun` → Taş-Kağıt-Makas oyunu"
    )


# ================== ANA PROGRAM ==================

async def main():
    await client.start()
    me = await client.get_me()
    print(f"Giriş yapıldı: {me.first_name} ({me.id})")

    await client.send_message("me", "✅ Bot başarıyla kuruldu!\n\nℹ️ `.artz help` yazarak komutları görebilirsin.")

    await client.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Kapatılıyor...")
