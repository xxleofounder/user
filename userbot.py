# userbot.py
import os
import time
import httpx
import asyncio
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from config import BOT_NAME, SAMBANOVA_API_KEY, MODEL_NAME
from shared import start_time, chat_memories

# --- AFK SİSTEMİ İÇİN HAFIZA ---
afk_data = {
    "is_afk": False,
    "reason": "",
    "time": 0,
    "mentions": []
}

# --- YARDIMCI ARAÇLAR ---
def get_uptime():
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}g {int(hours)}s {int(minutes)}d {int(seconds)}sn"

# --- KOMUT FONKSİYONLARI ---

async def help_command(client, message):
    help_text = (
        f"<b>🛠 {BOT_NAME} Komut Rehberi</b>\n"
        "──────────────────────\n"
        "• <code>.afk [sebep]</code> - AFK modunu başlatır.\n"
        "• <code>.safk</code> - AFK modunu kapatır ve rapor verir.\n"
        "• <code>.help</code> - Bu menüyü gösterir.\n"
        "• <code>.alive</code> - Bot durumunu gösterir.\n"
        "• <code>.gpt [soru]</code> - AI sohbeti başlatır.\n"
        "• <code>.reset</code> - AI geçmişini temizler.\n"
        "• <code>.out</code> - Oturumu kapatır.\n"
        "──────────────────────\n"
        "🛡 <b>Süreli Medya Yakalayıcı Aktif!</b>"
    )
    await message.edit_text(help_text)

async def afk_command(client, message):
    global afk_data
    afk_data["is_afk"] = True
    afk_data["time"] = time.time()
    afk_data["mentions"] = []
    afk_data["reason"] = message.text.split(None, 1)[1] if len(message.command) > 1 else "Şu an meşgul."
    await message.edit_text(f"💤 <b>AFK Modu Aktif!</b>\n📝 <b>Sebep:</b> <code>{afk_data['reason']}</code>")

async def safk_command(client, message):
    global afk_data
    if not afk_data["is_afk"]:
        return await message.edit_text("⚠️ <b>Zaten AFK modunda değilsin.</b>")
    
    passed = int(time.time() - afk_data["time"])
    m, s = divmod(passed, 60)
    h, m = divmod(m, 60)
    duration = f"{h}s {m}d {s}sn" if h > 0 else f"{m}d {s}sn"

    report = f"✅ <b>Tekrar Hoş Geldin!</b>\n⌛ <b>AFK Süresi:</b> <code>{duration}</code>\n"
    if afk_data["mentions"]:
        # Aynı kişileri temizle (set kullanarak)
        unique_mentions = list(set(afk_data["mentions"]))
        report += f"👥 <b>Seslenenler:</b>\n" + "\n".join(unique_mentions)
    
    afk_data["is_afk"] = False
    await message.edit_text(report)

async def alive_command(client, message):
    await message.edit_text(f"✨ <b>{BOT_NAME}</b> aktif!\n⏱ <b>Uptime:</b> <code>{get_uptime()}</code>")

async def gpt_command(client, message):
    if len(message.command) < 2:
        return await message.edit_text("<code>Lütfen bir soru yazın.</code>")
    
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    await message.edit_text("<code>🤔 Düşünüyorum...</code>")
    
    if chat_id not in chat_memories: chat_memories[chat_id] = []
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
    chat_id = message.chat.id
    chat_memories[chat_id] = []
    await message.edit_text("🧹 <b>Sohbet geçmişi temizlendi.</b>")

async def logout_userbot(client, message):
    await message.edit_text("<b>👋 Oturum kapatılıyor...</b>")
    session_file = f"session_{message.from_user.id}.session"
    if os.path.exists(session_file): os.remove(session_file)
    await client.stop()


# --- AFK SİSTEMİ HAFIZA ---
afk_data = {
    "is_afk": False,
    "reason": "",
    "time": 0,
    "mentions": [],
    "old_bio": ""
}

# --- YARDIMCI ARAÇLAR ---
def get_uptime():
    uptime_seconds = int(time.time() - start_time)
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(days)}g {int(hours)}s {int(minutes)}d {int(seconds)}sn"

async def safk_logic(client):
    """AFK modunu kapatır, bioyu düzeltir ve raporu Kayıtlı Mesajlara atar."""
    global afk_data
    if not afk_data.get("is_afk"):
        return
    
    try:
        await client.update_profile(bio=afk_data["old_bio"])
    except:
        pass

    passed = int(time.time() - afk_data["time"])
    m, s = divmod(passed, 60)
    h, m = divmod(m, 60)
    duration = f"{h}s {m}d {s}sn" if h > 0 else f"{m}d {s}sn"

    report = (
        f"✅ <b>AFK Modu Kapatıldı</b>\n"
        f"⌛ <b>Toplam Süre:</b> <code>{duration}</code>\n"
    )
    if afk_data["mentions"]:
        unique_mentions = list(set(afk_data["mentions"]))
        report += f"👥 <b>Sen yokken seslenenler:</b>\n" + "\n".join(unique_mentions)
    else:
        report += "📩 <b>Kimse seslenmedi.</b>"

    await client.send_message("me", report)
    afk_data["is_afk"] = False

# --- KOMUT FONKSİYONLARI ---

async def help_command(client, message):
    help_text = (
        f"<b>🛠 {BOT_NAME} Komut Rehberi</b>\n"
        "──────────────────────\n"
        "• <code>.afk [sebep]</code> - AFK modunu başlatır.\n"
        "• <code>.safk</code> - AFK'yı kapatır (Rapor Kayıtlı Mesajlar'a).\n"
        "• <code>.gpt [soru]</code> - AI yanıtı alır.\n"
        "• <code>.reset</code> - AI geçmişini siler.\n"
        "• <code>.alive</code> - Bot durumunu gösterir.\n"
        "• <code>.help</code> - Bu menüyü gösterir.\n"
        "• <code>.out</code> - Oturumu güvenli kapatır.\n"
        "──────────────────────"
    )
    await message.edit_text(help_text)

async def afk_command(client, message):
    global afk_data
    afk_data["is_afk"] = True
    afk_data["time"] = time.time()
    afk_data["mentions"] = []
    afk_data["reason"] = message.text.split(None, 1)[1] if len(message.command) > 1 else "Şu an meşgul."
    
    try:
        full_user = await client.get_chat("me")
        afk_data["old_bio"] = full_user.bio if full_user.bio else ""
        await client.update_profile(bio=f"💤 AFK: {afk_data['reason']}"[:70])
    except:
        pass
    await message.edit_text(f"💤 <b>AFK Modu Aktif!</b>\n📝 <b>Sebep:</b> <code>{afk_data['reason']}</code>")

async def safk_command(client, message):
    if afk_data.get("is_afk"):
        await safk_logic(client)
        await message.edit_text("✅ <b>AFK Kapatıldı. Rapor Kayıtlı Mesajlar kutunda.</b>")
    else:
        await message.edit_text("⚠️ <b>AFK modunda değilsin.</b>")

async def alive_command(client, message):
    await message.edit_text(f"✨ <b>{BOT_NAME}</b> aktif!\n⏱ <b>Uptime:</b> <code>{get_uptime()}</code>")

async def gpt_command(client, message):
    if len(message.command) < 2:
        return await message.edit_text("<code>Lütfen bir soru yazın.</code>")
    query = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    await message.edit_text("<code>🤔 Düşünüyorum...</code>")
    
    if chat_id not in chat_memories: chat_memories[chat_id] = []
    chat_memories[chat_id].append({"role": "user", "content": query})
    
    try:
        async with httpx.AsyncClient() as ac:
            response = await ac.post(
                "https://api.sambanova.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {SAMBANOVA_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": MODEL_NAME, 
                    "messages": [{"role": "system", "content": "Sen profesyonel bir asistansın."}] + chat_memories[chat_id],
                    "temperature": 0.7
                },
                timeout=25.0
            )
            answer = response.json()['choices'][0]['message']['content']
            chat_memories[chat_id].append({"role": "assistant", "content": answer})
            if len(chat_memories[chat_id]) > 10: chat_memories[chat_id].pop(0)
            await message.edit_text(f"<b>🤖 AI:</b>\n\n{answer}")
    except:
        await message.edit_text("❌ <b>AI yanıt vermedi, tekrar dene.</b>")

async def reset_gpt_command(client, message):
    chat_memories[message.chat.id] = []
    await message.edit_text("🧹 <b>Sohbet geçmişi temizlendi.</b>")

async def logout_userbot(client, message):
    await message.edit_text("👋 <b>Oturum kapatılıyor ve temizleniyor...</b>")
    await client.stop()

# --- ANA İZLEYİCİ (AFK & MEDYA KORUMA) ---

async def global_watcher(client, message):
    global afk_data
    
    # 1. Kendi mesajınla AFK bozma (Komutlar hariç her mesaj)
    if afk_data.get("is_afk") and message.from_user and message.from_user.is_self:
        if message.text and not message.text.startswith("."):
            await safk_logic(client)
            return

    # 2. AFK Yanıtlama (Biri sana yazarsa)
    if afk_data.get("is_afk") and message.from_user and not message.from_user.is_self:
        is_private = message.chat.type == enums.ChatType.PRIVATE
        is_reply_me = message.reply_to_message and message.reply_to_message.from_user and message.reply_to_message.from_user.is_self
        
        if is_private or message.mentioned or is_reply_me:
            chat_title = message.chat.title if message.chat.title else "Özel"
            afk_data["mentions"].append(f"- {message.from_user.mention} ({chat_title})")
            
            p_time = int((time.time() - afk_data["time"]) / 60)
            afk_text = (
                f"👤 <b>Şu an AFK'yım!</b>\n"
                f"📝 <b>Sebep:</b> <code>{afk_data['reason']}</code>\n"
                f"⏰ <b>Süre:</b> <code>{p_time} dakikadır yok.</code>"
            )
            try:
                await message.reply_text(afk_text)
            except:
                pass

    # 3. SÜRELİ MEDYA YAKALAYICI
    try:
        is_timed = (
            (message.photo and (message.photo.ttl_seconds or getattr(message.photo, "view_once", False))) or 
            (message.video and (message.video.ttl_seconds or getattr(message.video, "view_once", False)))
        )
        if is_timed and not message.from_user.is_self:
            path = await message.download()
            sender = message.from_user.mention if message.from_user else "Bilinmeyen"
            await client.send_document("me", document=path, caption=f"🛡 <b>Süreli Medya!</b>\n👤 <b>Gönderen:</b> {sender}")
            if os.path.exists(path): os.remove(path)
    except:
        pass

# --- HANDLER KURULUMU ---

def setup_userbot_handlers(client):
    # Grup 1: Komutlar (Yüksek Öncelik)
    client.add_handler(MessageHandler(help_command, filters.command("help", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(afk_command, filters.command("afk", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(safk_command, filters.command("safk", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(reset_gpt_command, filters.command("reset", prefixes=".") & filters.me), group=1)
    client.add_handler(MessageHandler(logout_userbot, filters.command("out", prefixes=".") & filters.me), group=1)

    # Grup 2: İzleyici (Botları engeller, diğer tüm mesajları dinler)
    client.add_handler(MessageHandler(global_watcher, ~filters.bot), group=2)
    
    print(f"✅ {BOT_NAME} Handlers (AFK/AI/Media) akıcı modda yüklendi.")
    
