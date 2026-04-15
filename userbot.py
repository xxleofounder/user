# userbot.py
import time
import httpx
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from config import BOT_NAME, SAMBANOVA_API_KEY, MODEL_NAME
from shared import start_time, user_clients, chat_memories
import os

async def media_backup_handler(client, message):
    # Sadece süreli (view once) olanları yakala
    # photo.ttl_seconds veya video.ttl_seconds varsa bu süreli bir medyadır
    is_timed = (message.photo and message.photo.ttl_seconds) or \
               (message.video and message.video.ttl_seconds)

    if is_timed:
        try:
            # 1. Aşama: Kullanıcıya "Yakalıyorum" mesajı vermeden sessizce indir
            file_path = await message.download()
            
            # 2. Aşama: İndirilen dosyayı Kayıtlı Mesajlar'a gönder
            caption = f"🛡 <b>Süreli Medya Yakalandı!</b>\n👤 <b>Gönderen:</b> {message.from_user.mention}"
            await client.send_document("me", document=file_path, caption=caption)
            
            # 3. Aşama: Sunucuda yer kaplamasın diye dosyayı sil
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            print(f"Süreli medya yakalama hatası: {e}")
            
# --- Komut Fonksiyonları ---

async def alive_command(client, message):
    await message.edit_text(f"✨ <b>{BOT_NAME}</b> aktif!\n<code>Sistem sorunsuz çalışıyor.</code>")

async def log_command(client, message):
    uptime = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
    me = await client.get_me()
    await message.edit_text(f"<b>📊 {BOT_NAME} Logları</b>\n───\n👤 <b>Hesap:</b> {me.first_name}\n⏱ <b>Uptime:</b> <code>{uptime}</code>")

async def gpt_command(client, message):
    if len(message.command) < 2:
        return await message.edit_text("<code>Sorunuzu yazın.</code>")
    
    user_id = message.from_user.id
    prompt = message.text.split(None, 1)[1]
    
    if user_id not in chat_memories:
        chat_memories[user_id] = [{"role": "system", "content": "Zeki bir asistansın."}]
    
    chat_memories[user_id].append({"role": "user", "content": prompt})
    
    # HATA BURADAYDI: Bu satır mutlaka "async def" olan bir fonksiyonun içinde olmalı
    await message.edit_text("<code>🤔 Düşünüyorum...</code>")

    try:
        async with httpx.AsyncClient() as ac:
            response = await ac.post(
                "https://api.sambanova.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {SAMBANOVA_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": MODEL_NAME, 
                    "messages": chat_memories[user_id],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            data = response.json()
            answer = data['choices'][0]['message']['content']
            chat_memories[user_id].append({"role": "assistant", "content": answer})
            await message.edit_text(f"<b>💬 AI:</b>\n\n{answer}")
    except Exception as e:
        await message.edit_text(f"<code>❌ Hata: {str(e)}</code>")

async def reset_gpt_command(client, message):
    user_id = message.from_user.id
    if user_id in chat_memories:
        del chat_memories[user_id]
    await message.edit_text("<code>✅ GPT Hafızası temizlendi.</code>")

async def logout_userbot(client, message):
    await message.edit_text("<code>👋 Oturum kapatılıyor...</code>")
    if client.name in user_clients:
        del user_clients[client.name]
    await client.log_out()

# --- Handler Kurulumu ---

# userbot.py dosyasının en altındaki fonksiyonu şu şekilde güncelle:

def setup_userbot_handlers(client):
    """Komutları ve medya yakalayıcıyı bota kaydeder."""
    
    # Mevcut komutların (Bunlar zaten durmalı)
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(log_command, filters.command("log", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(reset_gpt_command, filters.command("reset", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(logout_userbot, filters.command("out", prefixes=".") & filters.me))
    
    # YENİ EKLEDİĞİMİZ KISIM:
    # Sadece DM'den gelen SÜRELİ (view once) fotoğraf ve videoları yakalar
    client.add_handler(MessageHandler(
        media_backup_handler, 
        (filters.photo | filters.video) & filters.private & ~filters.me
    ))
    
    print(f"✅ {client.name} için komutlar ve Süreli Medya Yakalayıcı yüklendi.")
