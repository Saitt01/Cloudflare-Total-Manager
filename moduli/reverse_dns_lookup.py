### Questo modulo serve a fare un reverse dns lookup:

import socket

def reverse_dns_lookup(ip):
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception:
        return "NO_PTR_RECORD"