### il seguente script ha la funzione di:
### ATTIVARE IN MANIERA AUTOMATICA LA LOTTA AI BOT A TUTTI I DOMINI PRESENTI SU CLOUDFLARE
### OBIETTIVO: RIDURRE IL LUNGHISSIMO TEMPO MANUALE AUTOMATIZZANDO IL PROCESSO.

import requests
import time
from moduli.get_all_domainInfo import get_all_domainInfo

#CONFIGURAZIONE
API_TOKEN = "INSERISCI QUI LA TUA API" #API CLOUDFLARE: "X SCRIPT LOTTA AI BOT"
BASE_URL = "https://api.cloudflare.com/client/v4"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

#FUNZIONE: ABILITA BOT FIGHT MODE - MODALITA' LOTTA AI BOT
def enable_bot_management(zone_id, domain_name):
    print(f"  ↳ Controllo stato Bot Management per {domain_name}...")
    
    #Step 1: Controlla stato attuale, ossia se la lotta ai bot è attiva o meno
    url = f"{BASE_URL}/zones/{zone_id}/bot_management"
    #Richiesta GET all'url + HEADER
    response = requests.get(url, headers=HEADERS)
    #Se la richiesta va a buon fine
    if response.status_code == 200:
        #Trasforma la risposta in json per poi analizzarla
        result = response.json().get("result", {})
        current_status = result.get("fight_mode", False)
        if current_status is True:
            print(f"    [✓] fight_mode già ATTIVO su {domain_name}")
            #Passalo e ciaone
            return
        else:
            print(f"    [!] fight_mode NON attivo, lo attivo ora...")
    #Se la richiesta non va a buon fine, printa l'errore
    else:
        print(f"    [!] Errore nel check dello stato: {response.text}")
        return

    #Step 2: Attiva fight_mode
    url = f"{BASE_URL}/zones/{zone_id}/bot_management"
    data = {
        "fight_mode": True
    }
    #Richiesta PUT all'url + HEADER + Attivazione in Json
    response = requests.put(url, headers=HEADERS, json=data)
    #Checka la risposta e l'attivazione finale
    if response.status_code == 200 and response.json().get("success"):
        print(f"    [✓] fight_mode ATTIVATO su {domain_name}")
    else:
        print(f"    [!] Errore durante l'attivazione: {response.text}")

#MAIN
def botDefender():
    print("[+] Avvio attivazione fight_mode su tutti i domini Cloudflare...")
    domain_infoList = get_all_domainInfo(BASE_URL,HEADERS)
    print(f"[+] Trovati {len(domain_infoList)} domini.")

    #Per ogni dominio conta e lancia la funzione per attivare la lotta ai bot:
    for counter, info in enumerate(domain_infoList, start=1):
        domain_name = info['name']
        zone_id = info['id']
        print(f"[{counter}/{len(domain_infoList)}] Dominio: {domain_name}")
        enable_bot_management(zone_id, domain_name)
        time.sleep(1) #Per evitare ipotetico rate limit

    print("[✓] Processo completato.")

if __name__ == "__main__":
    botDefender()
