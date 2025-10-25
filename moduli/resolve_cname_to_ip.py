### Questo modulo serve a risolvere un CNAME in IP:

import socket

def resolve_cname_to_ip(cname):
    try:
        return socket.gethostbyname(cname)
    except Exception:
        return "CNAME_RESOLVE_FAIL"


