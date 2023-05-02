import csv
import maxminddb

# Path al file che contiene i dati del paese associati agli indirizzi IP
mmdb_file_path = "GeoLite2-Country.mmdb"


def get_continent(ip_address, reader):
    try:
        response = reader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        #response = reader.get(ip_address)
        #response = reader.country(ip_address)
        #response = reader.get(ip_address)
        #country = response.country
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

# Apri il file CSV con gli indirizzi IP
with open("indirizzi_ip.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    #next(csv_reader) # Salta la prima riga con l'intestazione
    ip_list = [row[0] for row in csv_reader]

# Carica il database MaxMindDB
reader = maxminddb.open_database(mmdb_file_path)

# Crea una lista di tuple con l'indirizzo IP e il paese associato
country_list = [(ip_address, get_continent(ip_address, reader), get_country(ip_address, reader)) for ip_address in ip_list]

# Chiudi il database MaxMindDB
reader.close()

# Scrivi i risultati su un nuovo file CSV
with open("indirizzi_ip_con_paese.csv", mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file, delimiter=",")
    writer.writerow(["Indirizzo IP", "Continente", "Paese"])
    for ip_address, country in country_list:
        writer.writerow([ip_address, country])