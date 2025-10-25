### Questo modulo serve ad automatizzare il processo di recupero info sui domini, in particolare è utile per le ZONE ID.

import time
import requests

def get_all_domainInfo(BASE_URL,HEADERS):
    domain_infoList = []
    page = 1
    while True:
        print(f"[+] Recupero pagina {page}...")
        #Creazione Url x richiesta API
        url = f"{BASE_URL}/zones?per_page=50&page={page}"
        #Richiesta GET all'url + HEADER
        response = requests.get(url, headers=HEADERS)
        #Risposta al GET
        data = response.json()
        
        if not data["result"]:
            break  #Se non ci sono risultati in "result" ferma, poiché significa che le pagine sono terminate
        
        #Aggiungi le liste dei valori dei domini quando si trovano e poi passa a pag. successiva
        domain_infoList.extend(data["result"])
        page += 1
        time.sleep(1)  #Per evitare ipotetico rate limit
    return domain_infoList

