# main.py
import logging
from pyrogram import Client, filters
from pyrogram.errors import (
    SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, 
    PhoneCodeExpired, FloodWait
)
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME
from shared import user_data, user_clients
from userbot import setup_userbot_handlers

# Hataları terminalde görmek için loglama
logging.basicConfig(level=logging.ERROR)

# Ana giriş botunu (Bot API) başlatıyoruz
bot = Client("login_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    chat_id = message.chat.id
    welcome_text = (
        f"<b>🚀 {BOT_NAME} Sistemine Hoş Geldiniz</b>\n"
        "──────────────────────\n"
        "<code>Aşağıdaki menüden kurulumu başlatarak UserBot'unuzu aktif edebilirsiniz.</code>"
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

    if data == "show_commands":
        cmd_text = (
            f"<b>📜 {BOT_NAME} Komutları</b>\n"
            "──────────────────────\n"
            "• <code>.alive</code> - Bot aktiflik testi.\n"
            "• <code>.gpt (soru)</code> - AI asistan.\n"
            "• <code>.reset</code> - AI hafızasını siler.\n"
            "• <code>.log</code> - Çalışma süresi.\n"
            "• <code>.out</code> - Oturumu kapatır.\n"
            "──────────────────────"
        )
        await callback_query.edit_message_text(cmd_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri Dön", callback_data="back_to_main")]]))

    elif data == "back_to_main":
        user_data[chat_id]["step"] = None
        welcome_text = (
            f"<b>🚀 {BOT_NAME} Sistemine Hoş Geldiniz</b>\n"
            "──────────────────────\n"
            "<code>Aşağıdaki menüden kurulumu başlatarak UserBot'unuzu aktif edebilirsiniz.</code>"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Kurulumu Başlat", callback_data="start_login")],
            [InlineKeyboardButton("📜 Komutlar Rehberi", callback_data="show_commands")]
        ])
        await callback_query.edit_message_text(welcome_text, reply_markup=buttons)

    elif data == "start_login":
        user_data[chat_id]["step"] = "phone"
        await callback_query.edit_message_text(
            "<b>📱 Numara Girişi</b>\n──────────────────────\n<code>Lütfen numaranızı yazın (+90...):</code>", 
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 İptal", callback_data="back_to_main")]])
        )

    elif data == "confirm_phone":
        phone = user_data[chat_id].get("phone")
        session_name = f"session_{chat_id}"
        await client.edit_message_text(chat_id, main_msg_id, "<code>⏳ Sunucuya bağlanılıyor...</code>")
        
        # Temiz başlangıç için eski objeyi siliyoruz
        if session_name in user_clients:
            del user_clients[session_name]
            
        user_clients[session_name] = Client(session_name, api_id=API_ID, api_hash=API_HASH)

        try:
            await user_clients[session_name].connect()
            code_info = await user_clients[session_name].send_code(phone)
            user_data[chat_id].update({"hash": code_info.phone_code_hash, "step": "code"})
            
            await client.edit_message_text(
                chat_id, main_msg_id, 
                f"<b>📩 Kod Gönderildi</b>\n──────────────────────\n<code>{phone} adresine gelen kodu yazın:</code>", 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 İptal", callback_data="back_to_main")]])
            )
        except Exception as e:
            await client.edit_message_text(chat_id, main_msg_id, f"<code>❌ Hata: {str(e)}</code>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Geri Dön", callback_data="back_to_main")]]))

@bot.on_message(filters.text & filters.private)
async def login_logic(client, message):
    chat_id = message.chat.id
    if chat_id not in user_data or not user_data[chat_id].get("step"): 
        return
    
    step = user_data[chat_id].get("step")
    main_msg_id = user_data[chat_id].get("main_msg_id")
    session_name = f"session_{chat_id}"
    
    try: await message.delete() # Terminal kirlenmesin diye numarayı/kodu siliyoruz
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
            await client.edit_message_text(chat_id, main_msg_id, f"<code>❌ Şifre Yanlış: {str(e)}</code>")

async def finalize_login(client, chat_id, main_msg_id, session_name):
    """Oturumu başarıyla tamamlar ve komutları aktif eder."""
    user_data[chat_id]["step"] = None
    
    # Kritik: Bağlantıyı kesip tertemiz bir Client objesiyle komutları yüklüyoruz
    if user_clients[session_name].is_connected:
        await user_clients[session_name].disconnect()
    
    user_clients[session_name] = Client(session_name, api_id=API_ID, api_hash=API_HASH)
    
    # Komutları userbot.py'den çekip yüklüyoruz
    setup_userbot_handlers(user_clients[session_name])
    
    # Artık Userbot tamamen hazır
    await user_clients[session_name].start()
    
    await client.edit_message_text(
        chat_id, main_msg_id, 
        f"<b>🎉 Tebrikler!</b>\n\n<code>UserBot başarıyla kuruldu. Artık komutları (.alive, .gpt) kullanabilirsiniz.</code>"
    )
    # Kendine bildirim gönder
    await user_clients[session_name].send_message("me", f"✅ <b>{BOT_NAME} Kurulumu Tamamlandı!</b>\nKomutları test etmek için <code>.alive</code> yazabilirsin.")

if __name__ == "__main__":
    print(f"--- {BOT_NAME} ÇALIŞIYOR ---")
    bot.run()
