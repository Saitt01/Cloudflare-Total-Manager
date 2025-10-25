### Il seguente script ha la funzione di:
### ESPORTARE IN UNA CARTELLA, VIA API, TUTTE LE CONFIGURAZIONI DEI DNS PRESENTI IN CLOUDFLARE, IN FORMATO ZONEFILES 
### OBIETTIVO: OTTENERE BACKUP DEI DNS PRONTO ALL'USO.

import requests 
import os
import subprocess
import time
import shutil
from datetime import datetime
from moduli.get_all_domainInfo import get_all_domainInfo
from moduli.upload_to_drive import upload_to_drive

#CONFIGURAZIONE
API_TOKEN = "INSERISCI QUI LA TUA API"  #API CLOUDFLARE: "X SCRIPT BACKUP DNS"
BASE_URL = "https://api.cloudflare.com/client/v4"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

RCLONE_CONF_PATH = os.path.expanduser("~/.config/rclone/rclone.conf")

#CARTELLA DI EXPORT: QUESTA SARA' LA CARTELLA CARICATA IN GOOGLE DRIVE, SARA' UNICA E AGGIORNATA AL PRESENTE, DANDO LA POSSIBILITA' GRAZIE A GOOGLE DRIVE VERIONING, DI VEDERE LO STORICO DEI FILE E QUINDI I SALVATAGGI PASSATI
EXPORT_DIR = "dnsCloudflareBackup"

#FUNZIONE: PULISCE LA CARTELLA DAI FILEZONE DEL BACKUP PRECEDENTE
def clean_export_dir():
    #Controlla se la cartella esiste, se esiste significa che dentro ci sono i file vecchi del backup precedente quindi li elimina
    if os.path.exists(EXPORT_DIR):
        print(f"[+] Pulizia cartella '{EXPORT_DIR}'...")
        shutil.rmtree(EXPORT_DIR)
    #Altrimenti ne crea una nuova subito
    os.makedirs(EXPORT_DIR)
    print(f"[✓] Cartella '{EXPORT_DIR}' pronta.")

#FUNZIONE: ESPORTA COFIG. DNS DA CLOUDFLARE IN ZONEFILES
def export_zonefile(zone_id, domain_name):
    print(f"  ↳ Esporto DNS per {domain_name}...")
    #Lancia l'ultimo richiesta a Cloudflare per esportare le config. DNS
    url = f"{BASE_URL}/zones/{zone_id}/dns_records/export"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        #Costruisce il percorso del file in cui salvare i dati
        filepath = os.path.join(EXPORT_DIR, f"{domain_name}.zone")
        #Apre file in mod. scrittura
        with open(filepath, "w") as f:
            #Scrive il contenuto della risposta HTTP
            f.write(response.text)
        print(f"    [✓] Salvato in {filepath}\n")
    else:
        print(f"    [!] Errore {response.status_code} su {domain_name}: {response.text}")

#MAIN:
def dnsExporter():
    print("[+] Inizio esportazione zone DNS da Cloudflare")
    #Pulizia filezone del backup precedente (saranno disponibili su Cloud)
    clean_export_dir()
    domain_infoList = get_all_domainInfo(BASE_URL,HEADERS)
    print(f"[+] Trovati {len(domain_infoList)} Domini totali")

    #Per ogni dominio conta e lancia la funzione per esportare le config. DNS
    for counter,info in enumerate(domain_infoList, start =1):
        print(f"[{counter}/{len(domain_infoList)}] Esportando le config. DNS di: {info['name']}")
        export_zonefile(info["id"], info["name"])
        time.sleep(1)  #Per evitare ipotetico rate limit

    print(f"[✓] Esportazione completata in '{EXPORT_DIR}'")

    #Carica sul drive
    upload_to_drive(EXPORT_DIR)

if __name__ == "__main__":
    dnsExporter()