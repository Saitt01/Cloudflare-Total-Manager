### Questo modulo serve ad uploadare una cartella tramite RCLONE su Google Drive.

import shutil
import os 
import subprocess

RCLONE_CONF_PATH = os.path.expanduser("~/.config/rclone/rclone.conf")

def upload_to_drive(EXPORT_DIR):
    print(f"[+] Avvio upload su Google Drive con rclone della cartella '{EXPORT_DIR}'...")

    #Verifica che rclone sia installato
    if shutil.which("rclone") is None:
        print("[!] ERRORE: rclone non è installato o non è stato trovato nel PATH.")
        return
    else:
        print(f"[✓] rclone trovato in: /root/.config/")
    #Check presenza file .conf
    if os.path.exists(RCLONE_CONF_PATH):
        print(f"[✓] rclone.conf trovato in: {RCLONE_CONF_PATH}")
    else:
        print(f"[!] ERRORE: rclone.conf non trovato in: {RCLONE_CONF_PATH}")

    try:
        result = subprocess.run(
            ["rclone", "copy", EXPORT_DIR, f"gdrive:{EXPORT_DIR}", "--update", "--quiet"],
            check=True
        )
        print("[✓] Upload completato con successo.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Errore durante l'upload con rclone: {e}")