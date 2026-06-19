import threading, time, re, random
from concurrent.futures import ThreadPoolExecutor, as_completed

PROXIES = []
running = True

def fetch_proxies():
    global PROXIES
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&anonymity=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt",
        "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt",
        "https://api.openproxylist.xyz/http.txt",
        "https://api.openproxylist.xyz/socks5.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/http.txt",
        "https://raw.githubusercontent.com/UserR3X/proxy-list/main/socks5.txt",
        "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/http.txt",
        "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/master/socks5.txt",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://www.proxy-list.download/api/v1/get?type=socks5",
        "https://spys.me/socks.txt",
        "https://spys.me/proxy.txt",
    ]
    for url in sources:
        try:
            r = __import__('requests').get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                for line in r.text.strip().split('\n'):
                    line = line.strip()
                    if line and ':' in line and not line.startswith('#') and len(line) < 40:
                        match = re.search(r'(\d+\.\d+\.\d+\.\d+:\d+)', line)
                        if match: PROXIES.append(match.group(1))
                        else: PROXIES.append(line)
        except: pass
    PROXIES = list(set(PROXIES))
    print(f"\033[92m[+] {len(PROXIES)} proxies loaded\033[0m")

def _validate_one(proxy):
    try:
        r = __import__('requests').get("http://httpbin.org/ip", proxies={"http": proxy, "https": proxy}, timeout=3)
        if r.status_code == 200: return proxy
    except: pass
    return None

def validate_proxies():
    global PROXIES
    if not PROXIES: return
    print(f"\033[93m[+] Validating proxies...\033[0m")
    valid = []
    with ThreadPoolExecutor(max_workers=200) as ex:
        futures = {ex.submit(_validate_one, p): p for p in PROXIES[:500]}
        for f in as_completed(futures):
            try:
                res = f.result(timeout=5)
                if res: valid.append(res)
            except: pass
    PROXIES = valid
    print(f"\033[92m[+] {len(PROXIES)} proxies valid\033[0m")

def get_proxy():
    return random.choice(PROXIES) if PROXIES else None

def auto_refresh_proxies():
    while running:
        time.sleep(300)
        if len(PROXIES) < 20:
            print(f"\033[93m[+] Refreshing proxies...\033[0m")
            fetch_proxies()
            validate_proxies()
