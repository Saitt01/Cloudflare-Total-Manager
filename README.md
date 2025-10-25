# Cloudflare Total Manager – by Saitt01

**Cloudflare Total Manager** è un tool scritto in **Python** che centralizza in un unico sistema tutte le automazioni realizzate tramite le **API ufficiali di Cloudflare**.  
Nasce per semplificare la gestione di più domini in modo scalabile, mantenendo i processi ordinati, automatizzati e versionati.

---

## Obiettivo

Il progetto unifica diversi script autonomi in un unico ecosistema modulare:

- **Dns Exporter**: esegue il backup automatico di tutti i DNS in formato `.zone` e li carica su Google Drive tramite `rclone`.
- **Bot Defender**: abilita la modalità *Bot Fight Mode* su tutti i domini Cloudflare.
- **Organizer & Formatter**: genera un file CSV con i record principali (A e CNAME) e informazioni aggiuntive come stato proxy, HTTP response e PTR.
- **Proxy Allineator**: allinea automaticamente lo stato di proxy tra record A e CNAME.
- **Drive Uploader**: gestisce l’upload incrementale su Google Drive tramite `rclone`.

Tutti i moduli sono orchestrati da un **controller principale** con interfaccia CLI interattiva.

---

## Struttura del progetto

- **main.py** – Controller principale con menù CLI  
- **script/**
  - `DnsExporter.py` – Esporta le zone DNS e le carica su Google Drive  
  - `BotDefender.py` – Abilita automaticamente il Bot Fight Mode su tutte le zone  
  - `Organizer.py` – Crea un CSV con i record @ e www, aggiungendo HTTP response e host PTR  
  - `ProxyAllineator.py` – Allinea lo stato di proxy tra A e CNAME  
- **moduli/**
  - `get_all_domainInfo.py` – Recupera tutte le zone Cloudflare e i relativi metadati  
  - `upload_to_drive.py` – Wrapper per Rclone per gestire l’upload automatico  
  - `get_http_status.py` – Analizza lo stato HTTP di un dominio  
  - `reverse_dns_lookup.py` – Esegue reverse lookup PTR  
  - `resolve_cname_to_ip.py` – Risolve un CNAME nel suo IP  

---
## Utilizzo
Per utilizzare il Tool, basterà installare i file e i requirements sul proprio dispositivo, aggiungere ai file presenti in script/ le proprie API Cloudflare e successivamente si potrà lanciare la funzione 'main.py' e seguire le chiare indicazioni.

---
## Documentazione:
https://developers.cloudflare.com/api/

---
## Licenza
Distribuito sotto licenza MIT.
Libero utilizzo per scopi personali, educativi e di automazione infrastrutturale.