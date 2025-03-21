import argparse
import os
import shutil
import tarfile
import urllib.error
import urllib.request

from pydantic import BaseModel, ValidationError
import yaml

from helpers.GeoIP2Helpers import generateCSVFromGeoIP2Module

config_path = 'config.yaml'

# Valori di default
default_lang: str = 'en'

default_edition_asn: str = "GeoLite2-ASN"
default_edition_city: str = "GeoLite2-City"
default_edition_country: str = "GeoLite2-Country"

class EditionsConfig(BaseModel):
    asn: str
    city: str
    country: str

class GeoIPUpdaterConfig(BaseModel):
    AccountID: str
    LicenseKey: str

class Config(BaseModel):
    Editions: EditionsConfig
    geoipupdater: GeoIPUpdaterConfig
    lang_code: str
    
def load_config(file_path: str) -> Config:
    """_summary_

    Args:
        file_path (str): _description_

    Returns:
        Config: _description_
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config(**data)
class MainArgs(argparse.Namespace):
    update: bool
    generate: bool
    
def modify_permissions(tarinfo):
    """Modifica i permessi dei file estratti."""
    #if tarinfo.isfile() and tarinfo.name.endswith('.mmdb'):
    #    tarinfo.mode = 0x644  # Imposta permessi lettura/scrittura per proprietario, lettura per altri
    return tarinfo

def update_mm_db(license_key: str, edition: str = "GeoLite2-ASN" ) -> None:
    suffix: str = "tar.gz"
    # Definisci il nome del file
    filename: str = "{}.{}".format(edition, suffix)
    filename_mmdb: str = "{}.{}".format(edition, "mmdb")
    url = "https://download.maxmind.com/app/geoip_download?license_key={}&edition_id={}&suffix=tar.gz".format(license_key, edition)
    
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
                    tar.extract(member, './'
                                #, filter=modify_permissions
                                )

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


                

def update_mm_dbs(license_key: str, asnEdition: str, cityEdition: str, countryEdition: str) -> None:
    update_mm_db(license_key, asnEdition)
    update_mm_db(license_key, cityEdition)
    update_mm_db(license_key, countryEdition)
    
def get_args(parser: argparse.ArgumentParser) -> MainArgs:
    main_args = MainArgs()
    return parser.parse_args(namespace=main_args)
    


# Creazione del parser
parser = argparse.ArgumentParser(description="Estrai i dati GeoIP2 con 2 librerie opzionali su CSV")

parser.add_argument('--update'
                    , action='store_true'
                    , help='Update MMDB database files from MaxMindDB API network'
                    )

parser.add_argument('--generate'
                    , action='store_true'
                    , help='Generate CSV.'
                    )

# Parsing degli argomenti
args = get_args(parser=parser)

# Leggi il file di configurazione YAML
try:
    lang_code = default_lang
    edition_asn = default_edition_asn
    edition_city = default_edition_city
    edition_country = default_edition_country
    config = load_config(config_path)
    edition_asn = config.Editions.asn
    edition_city = config.Editions.city
    edition_country = config.Editions.country
    
    if config.lang_code in ['it', 'de', 'en']:
        lang_code = config.lang_code

    else:
        print(f"Il valore di lingua nel file di configurazione {config_path} non è uno fra it, de, en. Usando il valore predefinito: {default_lang}")
        lang_code = default_lang
except ValidationError as e:
    print(f"File di configurazione {config_path} non valido.")
except FileNotFoundError:
    print(f"File di configurazione {config_path} non trovato. Usando il valore predefinito: {default_lang}")

if args.update:
    update_mm_dbs(config.geoipupdater.LicenseKey
                        , config.Editions.asn
                        , config.Editions.city
                        , config.Editions.country)

# Esempio di utilizzo del codice ISO della lingua
print(f"Il codice ISO della lingua è: {lang_code}")

#generateCSVFromGeoIP2Module(os.path.dirname(os.path.abspath(__file__)))
if args.generate:
    generateCSVFromGeoIP2Module(".")