### Il seguente script ha la funzione di:
### Esportare in un file CSV tutti i domini presenti in Cloudflare grazie alla sua API
### L'obiettivo è quello di ottenere dei record A e CNAME i nome di @ e www

import requests
import csv
import time
import os
from moduli.get_all_domainInfo import get_all_domainInfo
from moduli.reverse_dns_lookup import reverse_dns_lookup
from moduli.resolve_cname_to_ip import resolve_cname_to_ip
from moduli.get_http_status import get_http_status
from moduli.upload_to_drive import upload_to_drive  

#CONFIGURAZIONE
API_TOKEN = "INSERISCI QUI LA TUA API"
BASE_URL = "https://api.cloudflare.com/client/v4"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

#CARTELLA DI EXPORT: QUESTA SARA' LA CARTELLA CARICATA IN GOOGLE DRIVE, SARA' UNICA E AGGIORNATA AL PRESENTE, DANDO LA POSSIBILITA' GRAZIE A GOOGLE DRIVE VERIONING, DI VEDERE LO STORICO DEI FILE E QUINDI I SALVATAGGI PASSATI
EXPORT_DIR = "dnsCloudflareOrganizer"

#FUNZIONE PER PRENDERE I RECORD DNS
def get_dns_records(zone_id):
    url = f"{BASE_URL}/zones/{zone_id}/dns_records?per_page=100"
    response = requests.get(url, headers=HEADERS)
    return response.json()['result']

#MAIN:
def organizzer_and_formatter():
    #Se non esiste crea la cartella
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    all_zones = get_all_domainInfo(BASE_URL,HEADERS)
    output_csv = os.path.join(EXPORT_DIR, "dnsCloudflareOrganized.csv")
    host_output = os.path.join(EXPORT_DIR, "hostnameOrganized.txt")
    unique_hostmap = set()

    with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ['DOMINIO', 'RECORD', 'TIPO', 'VALORE', 'PROXY', 'TAG_HOSTNAME', 'HTTP_RESPONSE', 'CNAME_CONVERTED']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        total_zones = len(all_zones)
        for counter, zone in enumerate(all_zones, start=1):
            zone_id = zone['id']
            zone_name = zone['name']
            print(f"\n[{counter}/{total_zones}] Analizzo dominio: {zone_name}")

            try:
                records = get_dns_records(zone_id)
            except Exception as e:
                print(f"[!] Errore nel recupero DNS per {zone_name}: {e}")
                continue

            for record in records:
                full_name = record['name']
                record_type = record['type']
                record_value = record['content']
                proxied = record.get('proxied', False)

                if full_name == zone_name:
                    record_name = "@"
                elif full_name == f"www.{zone_name}":
                    record_name = "www"
                else:
                    continue

                if record_type not in ['A', 'CNAME']:
                    continue

                tag_hostname = ""
                http_status = ""
                cname_converted = ""

                if record_type == "A":
                    tag_hostname = reverse_dns_lookup(record_value)
                    http_status = get_http_status(zone_name)
                    if tag_hostname != "NO_PTR_RECORD":
                        unique_hostmap.add((record_value, tag_hostname))
                elif record_type == "CNAME":
                    cname_converted = resolve_cname_to_ip(record_value)

                writer.writerow({
                    'DOMINIO': zone_name,
                    'RECORD': record_name,
                    'TIPO': record_type,
                    'VALORE': record_value,
                    'PROXY': 'ATTIVA' if proxied else 'NON ATTIVA',
                    'TAG_HOSTNAME': tag_hostname,
                    'HTTP_RESPONSE': http_status,
                    'CNAME_CONVERTED': cname_converted
                })

                print(f"[✓] {record_name}.{zone_name} → {record_type} → {record_value} | HTTP: {http_status}")
                time.sleep(0.2)

    with open(host_output, "w", encoding="utf-8") as hostfile:
        for ip, hostname in sorted(unique_hostmap):
            hostfile.write(f"{ip} - {hostname}\n")

    print(f"\n[✓] Report finale CSV: {output_csv}")
    print(f"[✓] File hostname/IP: {host_output}")

if __name__ == "__main__":
    organizzer_and_formatter()
    upload_to_drive(EXPORT_DIR)