import csv
import os
import yaml
import maxminddb
from geoipupdate import GeoIpUpdater

# Path al file che contiene i dati del paese associati agli indirizzi IP
mmdb_file_path = "GeoLite2-City.mmdb"
mmdb_file_path_asn = "GeoLite2-ASN.mmdb"
# Funzione che restituisce il continente associato all'indirizzo IP
def get_continent(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        return response['continent']['names']['en']
    except KeyError:
        return "N/A"
    
# Funzione che restituisce il paese associato all'indirizzo IP
def get_country(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        #response = reader.get(ip_address)
        #response = reader.country(ip_address)
        #response = reader.get(ip_address)
        #country = response.country
        return response['country']['names']['en']
    except KeyError:
        return "N/A"

# Funzione che restituisce la citta' associata all'indirizzo IP
def get_city(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        return response['city']['names']['en']
    except KeyError:
        return "N/A"
    
def get_asn_autonomous_system_organization(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        return response['autonomous_system_organization']
    except KeyError:
        return "N/A"
    
def get_asn_autonomous_system_number(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        return response['autonomous_system_number']
    except KeyError:
        return "N/A"

    

#usage = "USAGE: %prog [-f license_file] [-d custom_directory]"
#version = "%prog Version {0}".format(_version)
#geoipupdater = OptionParser(usage=usage, version=version)
#licensekey, userid, editions = process_conf(options.license)

# Caricamento dei dati di configurazione da un file YAML
with open('config.yaml') as f:
    config = yaml.safe_load(f)

#licenseKey = config['geoipupdater']['LicenseKey']
#accountID = config['geoipupdater']['AccountID']
#editions = config['geoipupdater']['Editions']


#if not config['geoipupdater']['path']:
#    config['geoipupdater']['path'] = os.getcwd()

#updater = GeoIpUpdater(config['geoipupdater']['path'], licenseKey, accountID, editions, True)
#updater.update_databases()
#print("Run Complete")


# Apri il file CSV con gli indirizzi IP
with open("IP.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    #next(csv_reader) # Salta la prima riga con l'intestazione
    ip_list = [row[0] for row in csv_reader]

# Carica il database MaxMindDB
reader = maxminddb.open_database(mmdb_file_path)
reader_ASN = maxminddb.open_database(mmdb_file_path_asn)

# Crea una lista di tuple con l'indirizzo IP e il paese associato
geoip2_list = [
    (
    ip_address
    , get_continent(ip_address, reader)
    , get_country(ip_address, reader)
    , get_city(ip_address, reader)
    , get_asn_autonomous_system_number(ip_address, reader_ASN)
    , get_asn_autonomous_system_organization(ip_address, reader_ASN)
    ) for ip_address in ip_list
    ]

# Chiudi il database MaxMindDB
reader.close()

# Scrivi i risultati su un nuovo file CSV
with open("IP_con_geoip.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow([
        "IPAddress"
        , "Continent"
        , "Country"
        , "City"
        , "ASN-NUM"
        , "ASN-ORG"
        ])
    for ip_address, continent, country, city, asn_autonomous_system_num, asn_autonomous_system_organization in geoip2_list:
        writer.writerow([
            ip_address
            , continent
            , country
            , city
            , asn_autonomous_system_num
            , asn_autonomous_system_organization
            ])