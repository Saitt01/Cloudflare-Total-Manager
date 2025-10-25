### Questo modulo serve a salvare la risposta di un sito a una richiesta HTTP

import requests

def get_http_status(domain):
    headers = {"User-Agent": "Mozilla/5.0"}
    for scheme in ["http", "https"]:
        try:
            response = requests.head(f"{scheme}://{domain}", headers=headers, timeout=5, allow_redirects=True)
            return str(response.status_code)
        except requests.exceptions.Timeout:
            return "TIMEOUT"
        except Exception:
            continue
    return "NO_RESPONSE"