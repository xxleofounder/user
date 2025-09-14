import asyncio
import random
from telethon import TelegramClient, events, Button

api_id = 21883581
api_hash = 'c3b4ba58d5dada9bc8ce6c66e09f3f12'
bot_token = '8449988873:AAFAAdg4cwLjE2GtiBk891OfE85o-xRQVuc'

# Client oluştur
client = TelegramClient('uno_client', api_id, api_hash).start(bot_token=bot_token)

games = {}  # chat_id: game_data

# DM kontrol decorator
def only_in_group(func):
    async def wrapper(event):
        if event.is_private:
            await event.respond(
                "❌ Bu komut sadece gruplarda çalışır!",
                buttons=[[Button.url("Beni Gruba Ekle", "https://t.me/YOUR_BOT_USERNAME?startgroup=true")]]
            )
            return
        await func(event)
    return wrapper

# /start
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.is_private:
        await event.respond(
            "🎮 UNO Botuna Hoşgeldiniz!\n➡ Oyun oynamak için beni bir gruba ekleyin.",
            buttons=[
                [Button.url("Beni Gruba Ekle", "https://t.me/YOUR_BOT_USERNAME?startgroup=true")],
                [Button.inline("Help", data="help")]
            ]
        )

# Help inline
@client.on(events.CallbackQuery(data=b'help'))
async def help_button(event):
    await event.edit("ℹ️ UNO Bot Komutları:\n"
                     "/new - Yeni oyun başlat\n"
                     "/join - Oyuna katıl\n"
                     "🎴 Oyun sırasında:\nDraw - Kart çek\nPass - Sırayı geç\nPlay Card - Kart oyna\nWild kartlar renk seçimi ile oynanır",
                     buttons=[
                         [Button.inline("Geri", data="back")]
                     ])

@client.on(events.CallbackQuery(data=b'back'))
async def back(event):
    await event.edit("🎮 UNO Botuna Hoşgeldiniz!\n➡ Oyun oynamak için beni bir gruba ekleyin.",
                     buttons=[
                         [Button.url("Beni Gruba Ekle", "https://t.me/YOUR_BOT_USERNAME?startgroup=true")],
                         [Button.inline("Help", data="help")]
                     ])

# /new komutu - Lobby bekleme
@client.on(events.NewMessage(pattern='/new'))
@only_in_group
async def new_game(event):
    chat_id = event.chat_id
    if chat_id in games:
        await event.reply("❌ Zaten bir oyun devam ediyor!")
        return

    games[chat_id] = {'players': [], 'turn': 0, 'deck': [], 'current_card': None, 'hands': {}}
    lobby_msg = await event.reply("✅ Yeni UNO oyunu başlatıldı! Katılmak için /join yazın.\n⏳ 30 saniye lobby beklemesi...")

    # 30 saniye bekle
    for i in range(30, 0, -5):
        await asyncio.sleep(5)
        await lobby_msg.edit(f"✅ Yeni UNO oyunu başlatıldı! Katılmak için /join yazın.\n⏳ {i} saniye kaldı...")

    if len(games[chat_id]['players']) < 2:
        await lobby_msg.edit("❌ Yeterli oyuncu yok. Oyun iptal edildi.")
        del games[chat_id]
        return

    # Oyun başlıyor
    await lobby_msg.edit("🎉 Oyun Başlıyor!")

    # Kartlar
    colors = ['Red', 'Green', 'Blue', 'Yellow']
    special = ['Skip', 'Reverse', '+2']
    wild = ['Wild', '+4']
    deck = [f"{c} {n}" for c in colors for n in range(0,10)] + \
           [f"{c} {s}" for c in colors for s in special]*2 + wild*4
    random.shuffle(deck)
    games[chat_id]['deck'] = deck

    # Kart dağıtım animasyonu
    for player_id in games[chat_id]['players']:
        hand = [games[chat_id]['deck'].pop() for _ in range(7)]
        games[chat_id]['hands'][player_id] = hand
        hand_msg = await event.reply(f"🎴 {hand[0]}")
        for card in hand[1:]:
            await asyncio.sleep(0.3)
            await hand_msg.edit(hand_msg.text + f", {card}")

    # İlk kart
    first_card = games[chat_id]['deck'].pop()
    games[chat_id]['current_card'] = first_card
    await event.reply(f"🃏 İlk kart: {first_card}")

    # Sıra butonları
    current_player = games[chat_id]['players'][games[chat_id]['turn']]
    await event.reply(f"Sıradaki oyuncu: [{current_player}](tg://user?id={current_player})",
                      buttons=[
                          [Button.inline("Draw", data=f"draw_{current_player}"),
                           Button.inline("Pass", data=f"pass_{current_player}"),
                           Button.inline("Play Card", data=f"play_{current_player}")]
                      ])

# /join
@client.on(events.NewMessage(pattern='/join'))
@only_in_group
async def join_game(event):
    chat_id = event.chat_id
    user_id = event.sender_id

    if chat_id not in games:
        await event.reply("❌ Önce /new ile oyun başlatın.")
        return
    if user_id in games[chat_id]['players']:
        await event.reply("❌ Zaten oyundasınız!")
        return

    games[chat_id]['players'].append(user_id)
    await event.reply(f"✅ {event.sender.first_name} oyuna katıldı!")

# Draw / Pass / Play callback
@client.on(events.CallbackQuery)
async def button_handler(event):
    data = event.data.decode('utf-8')
    chat_id = event.chat_id

    if '_' not in data:  # Help veya başka inline
        return

    action, player_id = data.split('_')
    player_id = int(player_id)
    user_id = event.sender_id

    if chat_id not in games:
        await event.answer("❌ Oyun bulunamadı!", alert=True)
        return

    if user_id != player_id:
        await event.answer("❌ Sıra sizde değil!", alert=True)
        return

    if action == "draw":
        card = games[chat_id]['deck'].pop()
        games[chat_id]['hands'][user_id].append(card)
        await event.edit(f"🎴 Kart çekildi: {card}")
    elif action == "pass":
        await event.edit("⏭️ Sırayı geçtiniz.")
    elif action == "play":
        # Play Card mantığı basit demo
        hand = games[chat_id]['hands'][user_id]
        card_to_play = hand.pop(0)
        games[chat_id]['current_card'] = card_to_play
        await event.edit(f"🃏 Kart oynandı: {card_to_play}")

    # Sıradaki oyuncu
    games[chat_id]['turn'] = (games[chat_id]['turn'] + 1) % len(games[chat_id]['players'])
    next_player = games[chat_id]['players'][games[chat_id]['turn']]
    await event.respond(f"Sıradaki oyuncu: [{next_player}](tg://user?id={next_player})",
                        buttons=[
                            [Button.inline("Draw", data=f"draw_{next_player}"),
                             Button.inline("Pass", data=f"pass_{next_player}"),
                             Button.inline("Play Card", data=f"play_{next_player}")]
                        ])

print("UNO Client Botu çalışıyor...")
client.run_until_disconnected()
