# userbot.py
import time
import httpx
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from config import BOT_NAME, SAMBANOVA_API_KEY, MODEL_NAME
from shared import start_time, user_clients, chat_memories

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
    await message.edit_text("<code>🤔 Düşünüyorum...</code>")

    try:
        async with httpx.AsyncClient() as ac:
            response = await ac.post(
                "https://api.sambanova.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {SAMBANOVA_API_KEY}"},
                json={"model": MODEL_NAME, "messages": chat_memories[user_id]},
                timeout=30.0
            )
            answer = response.json()['choices'][0]['message']['content']
            chat_memories[user_id].append({"role": "assistant", "content": answer})
            await message.edit_text(f"<b>💬 AI:</b>\n\n{answer}")
    except Exception as e:
        await message.edit_text(f"<code>❌ Hata: {str(e)}</code>")

# --- KRİTİK KISIM: Handler Kurulumu ---
def setup_userbot_handlers(client):
    """Komutları bota kaydeder."""
    # Group=0 vererek en öncelikli sıraya alıyoruz
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me), group=0)
    client.add_handler(MessageHandler(log_command, filters.command("log", prefixes=".") & filters.me), group=0)
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me), group=0)
    
    print(f"✅ {client.name} için komutlar başarıyla yüklendi.")
    
    # Son 10 mesajı tut
    if len(chat_memories[user_id]) > 11: 
        chat_memories[user_id] = [chat_memories[user_id][0]] + chat_memories[user_id][-10:]

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
            answer = response.json()['choices'][0]['message']['content']
            chat_memories[user_id].append({"role": "assistant", "content": answer})
            await message.edit_text(f"<b>💬 {BOT_NAME} AI:</b>\n\n{answer}")
    except Exception as e:
        await message.edit_text(f"<code>❌ Hata: {str(e)}</code>")

async def reset_gpt_command(client, message):
    user_id = message.from_user.id
    if user_id in chat_memories: del chat_memories[user_id]
    await message.edit_text("<code>✅ GPT Hafızası temizlendi.</code>")

async def logout_userbot(client, message):
    await message.edit_text("<code>👋 Oturum kapatılıyor...</code>")
    if client.name in user_clients: del user_clients[client.name]
    await client.log_out()

def setup_userbot_handlers(client):
    client.add_handler(MessageHandler(alive_command, filters.command("alive", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(log_command, filters.command("log", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(gpt_command, filters.command("gpt", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(reset_gpt_command, filters.command("reset", prefixes=".") & filters.me))
    client.add_handler(MessageHandler(logout_userbot, filters.command("out", prefixes=".") & filters.me))
