import argparse
from helpers.GeoIP2Helpers import generateCSVFromGeoIP2Module
import os
import urllib.error
import urllib.request
import shutil
import tarfile
import yaml

config_path = 'config.yaml'

# Valori di default
default_lang: str = 'en'

default_edition_asn: str = "GeoLite2-ASN"
default_edition_city: str = "GeoLite2-City"
default_edition_country: str = "GeoLite2-Country"

# Leggi il file di configurazione YAML
try:
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError:
    print(f"File di configurazione {config_path} non trovato. Usando il valore predefinito: {default_lang}")
    lang_code = default_lang
    edition_asn = default_edition_asn
    edition_city = default_edition_city
    edition_country = default_edition_country
except:
    print(f"Errore durante la lettura del file di configurazione {config_path}. Usando il valore predefinito: {default_lang}")
    lang_code = default_lang
    edition_asn = default_edition_asn
    edition_city = default_edition_city
    edition_country = default_edition_country
else:
    edition_asn = config['Editions']['asn']
    edition_city = config['Editions']['city']
    edition_country = config['Editions']['country']
    # Controllo se il valore esiste e se è uno fra it, de, en

    #if config['geoipupdater']

    if 'lang_code' in config and config['lang_code'] in ['it', 'de', 'en']:
        lang_code = config['lang_code']

    else:
        print(f"Il valore di lingua nel file di configurazione {config_path} non è uno fra it, de, en. Usando il valore predefinito: {default_lang}")
        lang_code = default_lang

def updateMMDBDatabase(LicenseKey: str, edition: str = "GeoLite2-ASN" ) -> None:
    suffix: str = "tar.gz"
    # Definisci il nome del file
    filename: str = "{}.{}".format(edition, suffix)
    filename_mmdb: str = "{}.{}".format(edition, "mmdb")
    url = "https://download.maxmind.com/app/geoip_download?license_key={}&edition_id={}&suffix=tar.gz".format(LicenseKey, edition)
    
    try:
        retrieved = urllib.request.urlretrieve(url, filename)
    except urllib.error.HTTPError as e:
        print(f"Errore: {e}")
        return
    filename_mmdb: str = "{}.{}".format(edition, "mmdb")
    folderName: str = ""

    with tarfile.open(filename, 'r:gz') as tar:
        # Cicliamo su tutti i membri dell'archivio
        
        for member in tar.getmembers():
            if member.isdir():
                folderName = member.name
            # Verifichiamo se il membro corrente è un file
            if member.isfile():
                # Estraiamo solo i file di tipo .mmdb
                if os.path.splitext(member.name)[1] == '.mmdb':
                    # Estraiamo il file nella cartella corrente
                    tar.extract(member, './')

    # Definisci il percorso completo della sottocartella
    percorsoCartellaSorgente = os.path.join(os.getcwd(), folderName)

    # Definisci il percorso completo della cartella di destinazione
    percorsoCartellaDestinazione = os.getcwd()

    # Costruisci il percorso completo del file da spostare
    percorsoFileSorgente = os.path.join(percorsoCartellaSorgente, filename_mmdb)
    percorsoFileDestinazione = os.path.join(percorsoCartellaDestinazione, filename_mmdb)

    # Verifica se il file esiste il percorsoFileSorgente
    if os.path.exists(percorsoFileSorgente):
        if os.path.exists(percorsoFileDestinazione):
            os.remove(percorsoFileDestinazione)
        # Sposta il file nella cartella di destinazione
        shutil.move(percorsoFileSorgente, percorsoCartellaDestinazione)
        print("Il file è stato spostato con successo nella cartella di destinazione.")
        percorsoFileTarGz = os.path.join(os.getcwd(), filename)
        if os.path.exists(percorsoFileTarGz):
            os.remove(percorsoFileTarGz)
        if os.path.exists(percorsoCartellaSorgente):
            try:
                shutil.rmtree(percorsoCartellaSorgente)
                print("La cartella è stata rimossa con successo.")
            except PermissionError:
                print("Non hai i permessi sufficienti per rimuovere il file.")
            except FileNotFoundError:
                print("Il file non esiste.")
    else:
        print("Il file non esiste nella sottocartella.")


                

def updateMMDBDatabases(LicenseKey: str, asnEdition: str, cityEdition: str, countryEdition: str) -> None:
    updateMMDBDatabase(LicenseKey, asnEdition)
    updateMMDBDatabase(LicenseKey, cityEdition)
    updateMMDBDatabase(LicenseKey, countryEdition)
        
# Creazione del parser
parser = argparse.ArgumentParser(description="Estrai i dati GeoIP2 con 2 librerie opzionali su CSV")

parser.add_argument('--update'
                    , action='store_true'
                    , help='Update MMDB database files from MaxMindDB API network'
                    )

# Parsing degli argomenti
args = parser.parse_args()

if args.update:
    updateMMDBDatabases(config['geoipupdater']['LicenseKey'], config['Editions']['asn'], config['Editions']['city'], config['Editions']['country'])

# Esempio di utilizzo del codice ISO della lingua
print(f"Il codice ISO della lingua è: {lang_code}")

generateCSVFromGeoIP2Module()