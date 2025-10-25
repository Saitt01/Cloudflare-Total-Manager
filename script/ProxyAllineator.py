### TESTARE

import csv
import requests
from moduli.get_all_domainInfo import get_all_domainInfo

#CONFIGURAZIONE
API_TOKEN = "INSERISCI QUI LA TUA API"
BASE_URL = "https://api.cloudflare.com/client/v4"
CSV_PATH = "/opt/tool/cloudflareTotalManager/dns_report_enriched.csv"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

#FUNZIONE PER CREARE IL DIZIONARIO DELLE ZONE DISPONIBILI
def mapper_zone():
    zone_map = {}
    zone_list = get_all_domainInfo(BASE_URL, HEADERS)
    #Crea un dizionario per trovare velocemente le zone ID di ciascun dominio
    for zone in zone_list:
        name = zone["name"]  # es: 5terreliguri.com
        zone_map[name] = zone["id"]
    return zone_map

#FUNZIONE PER ANALIZZARE I DATI DEL CSV   
def csv_analyzer(csv_path):
    domains = {}
    #Apre ed analizza le colonne dominio e record
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=',')
        for row in reader:
            domain = row['DOMINIO']
            record = row['RECORD']
            if domain not in domains:
                domains[domain] = {}
            domains[domain][record] = row
    return domains

#FUNZIONE PER OTTENERE I RECORD ID
def get_record_id(zone_id, tipo, nome, valore):
    #Creazione Url
    url = f"{BASE_URL}/zones/{zone_id}/dns_records"
    params = {
        "type": tipo,
        "name": nome,
        "content": valore
    }
    #Manda richiesta GET
    response = requests.get(url, headers=HEADERS, params=params)
    #Prende risposta e la trasforma in JSON
    dati = response.json()
    if dati["success"] and dati["result"]:
        return dati["result"][0]["id"]
    return None

#FUNZIONE PER AGGIORNARE I PROXY:
def update_proxy(record, tipo, zone_id):
    nome = record['DOMINIO'] if record['RECORD'] == '@' else f"{record['RECORD']}.{record['DOMINIO']}"
    payload = {
        "type": tipo,
        "name": nome,
        "content": record["VALORE"],
        "ttl": 1,
        "proxied": True
    }

    record_id = get_record_id(zone_id, tipo, nome, record["VALORE"])
    if not record_id:
        print(f"[ERRORE] Impossibile trovare ID per {nome}")
        return

    url = f"{BASE_URL}/zones/{zone_id}/dns_records/{record_id}"
    response = requests.put(url, headers=HEADERS, json=payload)

    if response.status_code == 200 and response.json().get("success"):
        print(f"[+] Proxy attivato per {nome}")
    else:
        print(f"[ERRORE] Errore aggiornando {nome}: {response.text}")

#MAIN
def proxyAllineator():
    domains = csv_analyzer(CSV_PATH)
    zone_map = mapper_zone()

    for domain, records in domains.items():
        if domain not in zone_map:
            print(f"[ERRORE] Nessuna zona trovata per {domain}, saltato.")
            continue
        #Crea le variaibli per il confronto
        zone_id = zone_map[domain]
        record_root = records.get('@')
        record_www = records.get('www')

        if not record_root or not record_www:
            continue
        #IF con i paramentri dell'allineamento
        if record_root['PROXY'].upper() == "ATTIVA" and record_www['PROXY'].upper() == "NON ATTIVA":
            tipo = record_www['TIPO']
            if tipo in ['A', 'CNAME']:
                print(f"[→] www.{domain} risulta da allineare.")
                update_proxy(record_www, tipo, zone_id)
                print(f"[→] L'allineamento di www.{domain} è stato eseguito con successo.\n")
        else:
            print("Lo stato di proxy di tutti i domini è già allineato! :)")
            return
    
    print("Se sono avvenuti allineamenti, è oppurtuno rilanciare anche il DNS Exporter e l'Organizer per rimanere aggiornati!")

if __name__ == "__main__":
    proxyAllineator()
