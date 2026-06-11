#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import os, sys, socket, threading, json, urllib.request

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")

RS = "\033[0m"; R1 = "\033[38;5;196m"
GRY = "\033[38;5;245m"; DIM = "\033[38;5;240m"

def _clr(): os.system("cls" if os.name == "nt" else "clear")

def _get_ngrok():
    if not os.path.exists(ENV_PATH):
        return None
    with open(ENV_PATH) as f:
        for line in f:
            if line.startswith("NGROK_DOMAIN="):
                return line.strip().split("=", 1)[1]
    return None

def _check_ngrok_tunnel(port):
    try:
        r = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=3)
        data = json.loads(r.read())
        for t in data.get("tunnels", []):
            if f"localhost:{port}" in t.get("config", {}).get("addr", ""):
                return t.get("public_url", "")
    except: pass
    return None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ip = self.client_address[0]
        ua = self.headers.get("User-Agent", "?")
        ref = self.headers.get("Referer", "?")
        print(f"\n  [{datetime.now():%H:%M:%S}]  {R1}IP: {ip}{RS}")
        print(f"  {GRY}UA: {ua[:80]}{RS}")
        print(f"  {GRY}Ref: {ref[:80]}{RS}")
        print(f"  {DIM}Path: {self.path}{RS}\n")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")
    def log_message(self, *a): pass

if __name__ == "__main__":
    _clr()
    print(f"\n  {R1}IP LOGGER TEST{RS}  {DIM}VX SOCIETY{RS}\n")

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

    pub_url = _check_ngrok_tunnel(port)
    if pub_url:
        print(f"  {R1}Link:{RS}  {pub_url}")
    else:
        domain = _get_ngrok()
        if domain:
            print(f"  {R1}Link:{RS}  https://{domain}")
            print(f"  {DIM}(si ngrok no esta activo, no funcionara){RS}")
        else:
            print(f"  {R1}Link local (solo funciona en tu red):{RS}")
            host = socket.gethostbyname(socket.gethostname())
            print(f"  http://{host}:{port}")

    print(f"\n  {GRY}Puerto: {port}{RS}")
    print(f"  {GRY}Esperando visitas... Ctrl+C para salir{RS}\n")

    try:
        HTTPServer(("0.0.0.0", port), Handler).serve_forever()
    except KeyboardInterrupt:
        print(f"\n  {GRY}Finalizado{RS}\n")
    except OSError as e:
        print(f"\n  {R1}Error: {e}{RS}\n")
        print(f"  {GRY}El puerto {port} esta en uso. Usa: python3 iptest.py <puerto>{RS}\n")
