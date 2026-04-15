# userbot.py
import os
import time
import httpx
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import BOT_NAME, SAMBANOVA_API_KEY, MODEL_NAME
from shared import start_time, chat_memories

# --- YARDIMCI ARAÇLAR ---

def get_uptime():
    """Botun ne kadar süredir çalıştığını hesaplar."""
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}g {int(hours)}s {int(minutes)}d {int(seconds)}sn"

# --- KOMUT FONKSİYONLARI ---

async def help_command(client, message):
    """Kullanıcıya tüm komut listesini gösterir."""
    help_text = (
        f"<b>🛠 {BOT_NAME} Komut Rehberi</b>\n"
        "──────────────────────\n"
        "• <code>.help</code> - Bu menüyü gösterir.\n"
        "• <code>.alive</code> - Bot durumunu ve uptime süresini gösterir.\n"
        "• <code>.gpt [soru]</code> - Yapay zeka ile sohbet başlatır.\n"
        "• <code>.reset</code> - AI sohbet geçmişini temizler.\n"
        "• <code>.log</code> - Sistem bilgilerini detaylıca sunar.\n"
        "• <code>.out</code> - Oturumu kapatır ve verileri siler.\n"
        "──────────────────────\n"
        "🛡 <b>Süreli Medya Yakalayıcı:</b> Aktif (DM)"
    )
    await message.edit_text(help_text)

async def alive_command(client, message):
    """Botun hayatta olup olmadığını test eder."""
    await message.edit_text(
        f"✨ <b>{BOT_NAME}</b> aktif ve görevde!\n"
        f"⏱ <b>Çalışma Süresi:</b> <code>{get_uptime()}</code>"
    )

async def log_command(client, message):
    """Sistem istatistiklerini gösterir."""
    log_text = (
        f"<b>📊 {BOT_NAME} Sistem Durumu</b>\n"
        "──────────────────────\n"
        f"• <b>Sistem:</b> Linux VPS\n"
        f"• <b>Uptime:</b> <code>{get_uptime()}</code>\n"
        f"• <b>AI Model:</b> <code>{MODEL_NAME}</code>\n"
        f"• <b>Geliştirici:</b> Rahmet Pro\n"
        "──────────────────────"
    )
    await message.edit_text(log_text)

async def gpt_command(client, message):
    """AI üzerinden yanıt döndürür."""
    if len(message.command) < 2:
        return await message.edit_text("<code>Lütfen bir soru girin. Örn: .gpt nasılsın?</code>")

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
                    "messages": [{"role": "system", "content": "Sen Rahmet Pro tarafından geliştirilen profesyonel bir asistansın."}] + chat_memories[chat_id],
                    "temperature": 0.7
                },
                timeout=30.0
            )
            data = response.json()
            answer = data['choices'][0]['message']['content']
            
            chat_memories[chat_id].append({"role": "assistant", "content": answer})
            if len(chat_memories[chat_id]) > 10: chat_memories[chat_id].pop(0)

            await message.edit_text(f"<b>🤖 AI Yanıtı:</b>\n\n{answer}")
    except Exception as e:
        await message.edit_text(f"❌ <b>Hata:</b> <code>{str(e)}</code>")

async def reset_gpt_command(client, message):
    """Hafızayı sıfırlar."""
    chat_id = message.chat.id
    chat_memories[chat_id] = []
    await message.edit_text("🧹 <b>Zihin temizlendi!</b> Yeni bir sohbete başlayabiliriz.")

async def logout_userbot(client, message):
    """Oturumu sonlandırır."""
    await message.edit_text("<b>👋 Görüşmek üzere! Oturum kapatılıyor...</b>")
    # Mevcut session dosyasını bulup siliyoruz
    session_file = f"session_{message.from_user.id}.session"
    if os.path.exists(session_file):
        os.remove(session_file)
    await client.stop()

async def media_backup_handler(client, message):
    """Hem saniyeli hem de 'tek seferlik' (view once) medyaları yakalar."""
    try:
        # 1. Kontrol: Saniye ayarı var mı?
        has_ttl = (
            (message.photo and message.photo.ttl_seconds) or 
            (message.video and message.video.ttl_seconds)
        )
        
        # 2. Kontrol: Tek seferlik (View Once) bayrağı aktif mi?
        # Bazı Pyrogram sürümlerinde .view_once veya .one_time_media olarak geçer
        is_view_once = getattr(message.photo, "view_once", False) or \
                       getattr(message.video, "view_once", False)

        # İki durumdan biri varsa yakala
        if has_ttl or is_view_once:
            # Sessizce indir
            file_path = await message.download()
            
            sender = message.from_user.mention if message.from_user else "Bilinmeyen Kullanıcı"
            
            # Başlık bilgisini ayarla
            media_type = "Fotoğraf" if message.photo else "Video"
            caption = f"🛡 <b>Süreli/Tek Seferlik {media_type} Yakalandı!</b>\n👤 <b>Gönderen:</b> {sender}"
            
            # Kayıtlı Mesajlar'a (Saved Messages) belge olarak gönder
            await client.send_document("me", document=file_path, caption=caption)
            
            # Sunucuda yer kaplamasın diye dosyayı sil
            if os.path.exists(file_path):
                os.remove(file_path)
                
    except Exception as e:
        print(f"Yakalayıcı Hatası: {e}")
            
# --- HANDLER KURULUMU ---


# userbot.py içine eklenecekler
import time
from pyrogram import filters
from pyrogram.handlers import MessageHandler
import shared

# --- AFK KOMUTLARI ---

async def afk_handler(client, message):
    shared.is_afk = True
    shared.afk_time = time.time()
    shared.afk_mentions = [] # Listeyi sıfırla
    
    # Sebep belirtilmemişse varsayılan ata
    if len(message.command) > 1:
        shared.afk_reason = message.text.split(None, 1)[1]
    else:
        shared.afk_reason = "Şu an meşgul."
        
    await message.edit_text(f"💤 <b>AFK Modu Aktif!</b>\n📝 <b>Sebep:</b> <code>{shared.afk_reason}</code>")

async def safk_handler(client, message):
    if not shared.is_afk:
        return await message.edit_text("⚠️ <b>Zaten AFK modunda değilsin.</b>")
    
    # Geçen süreyi hesapla
    uptime = int(time.time() - shared.afk_time)
    m, s = divmod(uptime, 60)
    h, m = divmod(m, 60)
    duration = f"{h}s {m}d {s}sn" if h > 0 else f"{m}d {s}sn"

    report = f"✅ <b>Geri geldin!</b>\n⌛ <b>AFK Süresi:</b> <code>{duration}</code>\n"
    
    if shared.afk_mentions:
        report += f"👥 <b>Sen yokken seslenenler:</b>\n" + "\n".join(list(set(shared.afk_mentions)))
    else:
        report += "📩 <b>Sen yokken kimse seslenmedi.</b>"
        
    shared.is_afk = False
    shared.afk_reason = ""
    await message.edit_text(report)

# --- AFK MESAJ TAKİPÇİSİ ---

async def afk_watcher_handler(client, message):
    # Eğer AFK isek ve gelen mesaj bizeyse (veya etiketse)
    if not shared.is_afk:
        return

    # Kendi yazdığımız mesajla AFK'yı bozma (Komut değilse)
    if message.from_user and message.from_user.is_self:
        if not message.text.startswith(".safk"):
            await safk_handler(client, message)
        return

    # Birisi bize DM atarsa veya bizi etiketlerse (Mention)
    is_mention = message.mentioned or (message.chat.type == "private" and not message.from_user.is_self)
    
    if is_mention and message.from_user:
        user = message.from_user
        shared.afk_mentions.append(f"- {user.mention} ({message.chat.title or 'DM'})")
        
        # Otomatik cevap ver
        afk_text = (
            f"👤 <b>Sahibim Şu An AFK!</b>\n"
            f"📝 <b>Sebep:</b> <code>{shared.afk_reason}</code>\n"
            f"⏰ <b>Süre:</b> <code>{int((time.time() - shared.afk_time)/60)} dakikadır yok.</code>"
        )
        await message.reply_text(afk_text)

# --- HANDLER KURULUMU ---
def setup_userbot_handlers(client):
    # Komutlar
    client.add_handler(MessageHandler(afk_handler, filters.command("afk", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(safk_handler, filters.command("safk", prefixes=".") & filters.me))
    
    # AFK İzleyici (Her mesajı kontrol eder)
    client.add_handler(MessageHandler(afk_watcher_handler, (filters.mentioned | filters.private) & ~filters.bot))
    
    # ... (Diğer .help, .alive vb. handlerların burada kalsın)
    


def setup_userbot_handlers(client):
    """Tüm komutları ve medya dinleyiciyi bota tanıtır."""
    
    # Komutlar (Prefix: '.')
    client.add_handler(MessageHandler(help_command, filters.command("help", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(log_command, filters.command("log", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(reset_gpt_command, filters.command("reset", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(logout_userbot, filters.command("out", prefixes=".") & filters.me))

    # Medya Yakalayıcı (Sadece DM üzerinden gelen başkasına ait süreli medyalar)
    client.add_handler(MessageHandler(
        media_backup_handler, 
        (filters.photo | filters.video) & filters.private & ~filters.me
    ))

    print(f"✅ {client.name} için tüm komutlar ve koruma sistemleri aktif!")
    
