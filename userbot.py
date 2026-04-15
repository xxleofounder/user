# userbot.py
import os
import time
import httpx
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from config import BOT_NAME, SAMBANOVA_API_KEY, MODEL_NAME
from shared import start_time, chat_memories

# --- YARDIMCI FONKSİYONLAR ---

def get_uptime():
    """Botun ne kadar süredir açık olduğunu hesaplar."""
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}g {int(hours)}s {int(minutes)}d {int(seconds)}sn"

# --- KOMUT FONKSİYONLARI ---

async def help_command(client, message):
    """Tüm komutları listeler."""
    help_text = (
        f"<b>🛠 {BOT_NAME} Komut Rehberi</b>\n"
        "──────────────────────\n"
        "• <code>.help</code> - Bu menüyü gösterir.\n"
        "• <code>.alive</code> - Botun durumunu kontrol eder.\n"
        "• <code>.gpt [soru]</code> - AI Asistanına soru sorar.\n"
        "• <code>.reset</code> - AI sohbet geçmişini siler.\n"
        "• <code>.log</code> - Çalışma süresi ve istatistikler.\n"
        "• <code>.out</code> - Oturumu güvenli şekilde kapatır.\n"
        "──────────────────────\n"
        "🛡 <b>Özellik:</b> Süreli Medya Yakalayıcı Aktif!"
    )
    await message.edit_text(help_text)

async def alive_command(client, message):
    """Aktiflik testi."""
    await message.edit_text(f"✨ <b>{BOT_NAME}</b> sorunsuz çalışıyor!\n⏱ <b>Uptime:</b> <code>{get_uptime()}</code>")

async def log_command(client, message):
    """Sistem bilgilerini gösterir."""
    log_text = (
        f"<b>📊 {BOT_NAME} Sistem Logları</b>\n"
        "──────────────────────\n"
        f"• <b>Durum:</b> Çevrimiçi\n"
        f"• <b>Çalışma Süresi:</b> <code>{get_uptime()}</code>\n"
        f"• <b>AI Modeli:</b> <code>{MODEL_NAME}</code>\n"
        f"• <b>Sunucu:</b> Linux VPS\n"
        "──────────────────────"
    )
    await message.edit_text(log_text)

async def gpt_command(client, message):
    """SambaNova üzerinden AI yanıtı döndürür."""
    if len(message.command) < 2:
        return await message.edit_text("<code>Lütfen bir soru yazın! Örn: .gpt nasılsın?</code>")

    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    await message.edit_text("<code>🤔 Düşünüyorum...</code>")

    if chat_id not in chat_memories:
        chat_memories[chat_id] = []

    chat_memories[chat_id].append({"role": "user", "content": query})

    try:
        async with httpx.AsyncClient() as ac:
            response = await ac.post(
                "https://api.sambanova.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {SAMBANOVA_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": MODEL_NAME,
                    "messages": [{"role": "system", "content": "Sen Rahmet Pro tarafından geliştirilen bir asistansın."}] + chat_memories[chat_id],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            data = response.json()
            answer = data['choices'][0]['message']['content']
            
            chat_memories[chat_id].append({"role": "assistant", "content": answer})
            if len(chat_memories[chat_id]) > 10: chat_memories[chat_id].pop(0)

            await message.edit_text(f"<b>🤖 AI Asistan:</b>\n\n{answer}")
    except Exception as e:
        await message.edit_text(f"❌ <b>Hata:</b> <code>{str(e)}</code>")

async def reset_gpt_command(client, message):
    """AI hafızasını temizler."""
    chat_id = message.chat.id
    if chat_id in chat_memories:
        chat_memories[chat_id] = []
    await message.edit_text("🧹 <b>Sohbet geçmişi bu sohbet için temizlendi.</b>")

async def logout_userbot(client, message):
    """Oturumu sonlandırır ve dosyayı siler."""
    await message.edit_text("<b>👋 Oturum kapatılıyor ve veriler siliniyor...</b>")
    session_file = f"session_{message.from_user.id}.session"
    if os.path.exists(session_file):
        os.remove(session_file)
    await client.stop()

# --- SÜRELİ MEDYA YAKALAYICI ---

async def media_backup_handler(client, message):
    """Süreli fotoğraf ve videoları yakalar."""
    try:
        # Medya süreli mi (ttl_seconds varsa sürelidir)
        is_timed = (message.photo and message.photo.ttl_seconds) or \
                   (message.video and message.video.ttl_seconds)

        if is_timed:
            # Sessizce indir
            file_path = await message.download()
            sender = message.from_user.mention if message.from_user else "Gizli Kullanıcı"
            caption = f"🛡 <b>Süreli Medya Yakalandı!</b>\n👤 <b>Gönderen:</b> {sender}"
            
            # Kayıtlı Mesajlar'a belge olarak gönder (Silinmemesi için)
            await client.send_document("me", document=file_path, caption=caption)
            
            # Sunucudan temizle
            if os.path.exists(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Medya Yakalama Hatası: {e}")

# --- HANDLER KURULUMU ---

def setup_userbot_handlers(client):
    """Tüm komutları ve olayları bota kaydeder."""
    
    # Komutlar (Sadece senin yazdığın . ile başlayanlar)
    client.add_handler(MessageHandler(help_command, filters.command("help", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(log_command, filters.command("log", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(reset_gpt_command, filters.command("reset", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(logout_userbot, filters.command("out", prefixes=".") & filters.me))

    # Medya Yakalayıcı (Özel mesajda başkasından gelen süreli medyalar)
    client.add_handler(MessageHandler(
        media_backup_handler, 
        (filters.photo | filters.video) & filters.private & ~filters.me
    ))

    print(f"✅ {client.name} için tüm komutlar yüklendi!")
    
