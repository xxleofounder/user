from telethon import TelegramClient, events
import asyncio

# ---- CONFIG ----
API_ID = 21883581
API_HASH = "c3b4ba58d5dada9bc8ce6c66e09f3f12"
MAIN_BOT_TOKEN = "8449988873:AAFAAdg4cwLjE2GtiBk891OfE85o-xRQVuc"

MAIN_START_MSG = "👋 Merhaba! Ben ana botum.\n/token <BOT_TOKEN> ile yeni bot ekleyebilirsin."
CLONE_START_MSG = "🤖 Selam! Ben yeni eklenen bir kopya botum."
# ----------------

# Ana bot client
main_bot = TelegramClient("main_bot", API_ID, API_HASH).start(bot_token=MAIN_BOT_TOKEN)

# Dinamik botları tutmak için dict
clone_bots = {}


# Ana botun start
@main_bot.on(events.NewMessage(pattern="^/start$"))
async def start_handler(event):
    await event.reply(MAIN_START_MSG)


# Ana botun help
@main_bot.on(events.NewMessage(pattern="^/help$"))
async def help_handler(event):
    await event.reply("/token <BOT_TOKEN> - Yeni bir kopya bot ekler.")


# Ana botun token komutu
@main_bot.on(events.NewMessage(pattern=r"^/token (.+)"))
async def token_handler(event):
    bot_token = event.pattern_match.group(1).strip()
    chat_id = event.chat_id

    try:
        # Yeni botu başlat
        clone = TelegramClient(f"clone_{bot_token}", API_ID, API_HASH)
        await clone.start(bot_token=bot_token)

        # Yeni bot sadece /start komutunu dinlesin
        @clone.on(events.NewMessage(pattern="^/start$"))
        async def clone_start_handler(ev):
            await ev.reply(CLONE_START_MSG)

        # Listede sakla
        clone_bots[bot_token] = clone

        await event.reply("✅ Yeni bot eklendi ve çalışıyor.")
        await clone.send_message(chat_id, CLONE_START_MSG)

        # Botları arka planda çalıştır
        asyncio.create_task(clone.run_until_disconnected())

    except Exception as e:
        await event.reply(f"❌ Hata: {e}")


print("🚀 Ana bot çalışıyor...")
main_bot.run_until_disconnected()
