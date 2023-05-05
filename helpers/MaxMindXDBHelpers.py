import csv
import maxminddb.types

# Funzione che restituisce il continente associato all'indirizzo IP
def get_continent(ip_address: str, maxminddbReader: maxminddb.Reader, lang: str) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['continent']['names'][lang]
    except KeyError:
        return "N/A"
    

    
# Funzione che restituisce il paese associato all'indirizzo IP
def get_country(ip_address, maxminddbReader: maxminddb.Reader, lang: str) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['country']['names'][lang]
    except KeyError:
        return "N/A"




# Funzione che restituisce la citta' associata all'indirizzo IP
def get_city(ip_address, maxminddbReader: maxminddb.Reader, lang: str) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['city']['names'][lang]
    except KeyError:
        return "N/A"


    
def get_asn_autonomous_system_number(ip_address, maxminddbReader: maxminddb.Reader) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['autonomous_system_number']
    except KeyError:
        return "N/A"


    
def get_asn_autonomous_system_organization(ip_address, maxminddbReader: maxminddb.Reader) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['autonomous_system_organization']
    except KeyError:
        return "N/A"



# Funzione che restituisce la location associata all'indirizzo IP
def get_latitude(ip_address, maxminddbReader: maxminddb.Reader) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['city']['location']['latitude']
    except KeyError:
        return "N/A"
    
def get_longitude(ip_address, maxminddbReader: maxminddb.Reader) -> str:
    try:
        maxminddbRecord: maxminddb.types.Record = maxminddbReader.get(ip_address)    
    except ValueError:
        return "N/A"
    
    try:
        if maxminddbRecord==None:
            return "N/A"
        else:
            return maxminddbRecord['city']['location']['latitude']
    except KeyError:
        return "N/A"

def generateCSVFromMaxMindModule(lang: str="en", inputCSVFileName: str="IP.csv", outputCSVFileName: str="IP_con_geoip.csv"):
    # Apri il file CSV con gli indirizzi IP
    try:
        with open(inputCSVFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader) # Salta la prima riga con l'intestazione
            ip_list = [row[0] for row in csv_reader]
    except IOError:
        print(f"Errore durante l'apertura del file CSV '{inputCSVFileName}'")
        return

    #Scrivi i risultati su un nuovo file CSV utilizzando MaxMindDB DatabaseReader
    with open(outputCSVFileName, mode="w", newline="", encoding="utf-8") as csv_file:
        # Carica il database MaxMindDB
        maxminddbReader_ASN = maxminddb.Reader("GeoLite2-ASN.mmdb")
        maxminddbReader_City = maxminddb.Reader("GeoLite2-City.mmdb")
        maxminddbReader_Country = maxminddb.Reader("GeoLite2-Country.mmdb")
        # Crea una lista di tuple
        maxminddb_list = [
        (
        ip_address
        , get_continent(ip_address, maxminddbReader_City, lang)
        , get_country(ip_address, maxminddbReader_City, lang)
        , get_city(ip_address, maxminddbReader_City, lang)
        , get_asn_autonomous_system_number(ip_address, maxminddbReader_ASN)
        , get_asn_autonomous_system_organization(ip_address, maxminddbReader_ASN)
        , get_latitude(ip_address, maxminddbReader_City)
        , get_longitude(ip_address, maxminddbReader_City)
        ) for ip_address in ip_list
        ]

        # Chiudi i Reader MaxMindDB
        maxminddbReader_ASN.close()
        maxminddbReader_City.close()
        maxminddbReader_Country.close()

        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow([
            "IPAddress"
            , "Continent"
            , "Country"
            , "City"
            , "ASN-NUM"
            , "ASN-ORG"
            , "Latitude"
            , "Longitude"
            ])
        for ip_address, continent, country, city, asn_autonomous_system_num, asn_autonomous_system_org, latitude, longitude in maxminddb_list:
            writer.writerow([
                ip_address
                , continent
                , country
                , city
                , asn_autonomous_system_num
                , asn_autonomous_system_org
                , latitude
                , longitude
                ])
        csv_file.close()