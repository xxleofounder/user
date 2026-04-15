# shared.py
import time

# Kullanıcı verileri ve oturum açmış clientlar
user_data = {}
user_clients = {}

# Konuşma geçmişi (Hafızalı GPT için)
chat_memories = {}

# Botun başlangıç zamanı
start_time = time.time()

# shared.py içine eklenecekler
is_afk = False
afk_reason = ""
afk_time = 0
afk_mentions = [] # Sen yokken seni etiketleyenlerin listesi
