### Questo è il file centrale di controllo e gestione di tutti gli scirpt di cloudflareTotalManager

from script.DnsExporter import dnsExporter
from script.BotDefender import botDefender
from script.Organizer import organizzer_and_formatter 
from script.ProxyAllineator import proxyAllineator
import subprocess

def print_ascii_banner():
    banner = subprocess.check_output(["figlet", "CloudflareTM"]).decode()
    print(banner)

###PER AGGIUNGERE NUOVI SCRIPT E FUNZIONALITA' EXTRA:
def manage_input():
    action = input("Seleziona il servizio che vuoi utilizzare:\n[1]=== Dns Exporter\n[2]=== Bot Defender\n[3]=== Organizer\n[4]=== Proxy Allineator\n[i]=== Maggiori Info\nInserisci il numero del servizio: \n")
    if action == "i":
        print("[1]=== Dns Exporter:\nServe ad esportare in Google Cloud i file.zone di ogni dominio presente in Cloudflare.\n[2]=== Bot Defender:\nServe ad attivare la modalità 'Lotta ai Bot' in ogni dominio presente su Cloudflare\n[3]=== Organizer:\nServe ad ottenere un file csv con i valori dei Record,Name,Http Response, ed altre \ninformazioni, per poi poter svolgere azioni e analisi massive su essi,\nprinterà inoltre anche un file txt con tutti gli hostname presenti in Cloudflare\n[4]=== Proxy Allineator:\nServe ad allineare lo stato di proxy dei CNAME ai record A")
        manage_input()
    elif action == "1":
        dnsExporter()
        loop_manage_input()
    elif action == "2":
        botDefender()
        loop_manage_input()
    elif action == "3":
        organizzer_and_formatter()
        loop_manage_input()
    elif action == "4":
        proxyAllineator()
        loop_manage_input()
    ###AGGIUNGI QUI IN CASO UN NUOVO ELIF X SERVIZIO EXTRA, E RICORDATI DI AGGIUNGERLO ANCHE IN ACTION.
    else:
        print("Inserisci solo ed unicamente il numero del servizio che vuoi utilizzare!\n")
        manage_input()

#GESTISCE CIO' CHE AVVIENE DOPO IL PRIMO SERVIZIO EFFETTUATO, SE CONTINUARE CON UN ALTRO O CHIUDERE IL SOFTWARE
def loop_manage_input():
    what_else = input("\n\n\n[+]Vuoi utilizzare un altro servizio?\n[1]=== SI\n[2]=== NO, esci\nInserisci il numero della risposta: \n")
    if what_else == "1":
        manage_input()
    elif what_else == "2":
        print("Ciao, a presto! :)")
    else:
        print("Inserisci solo ed unicamente il numero della rìsposta che vuoi scegliere!\n")
        loop_manage_input()

#MAIN       
def main():
    print_ascii_banner()
    manage_input()

if __name__ == "__main__":
    main()