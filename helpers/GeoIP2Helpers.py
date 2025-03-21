import csv
import geoip2.database
import geoip2.errors
import geoip2.models
import geoip2.types
import os
import sys

def get_country_geoip2_record(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader) -> geoip2.models.Country:
    try:
        return geoip2Reader.country(ip_address)
    except geoip2.errors.AddressNotFoundError as e:
        print(f"{e} (DB Country)")

def get_city_geoip2_record(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader) -> geoip2.models.City:
    try:
        return geoip2Reader.city(ip_address)
    except geoip2.errors.AddressNotFoundError as e:
        print(f"{e} (DB City)")

def get_asn_geoip2_record(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader) -> geoip2.models.ASN:
    try:
        return geoip2Reader.asn(ip_address)
    except geoip2.errors.AddressNotFoundError as e:
        print(f"{e} (DB ASN)")

def get_continent(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader, lang: str) -> str:
    try:
        countryModelRecord: geoip2.models.Country = get_country_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if countryModelRecord==None:
            return "N/A"
        else:
            return countryModelRecord.continent.names[lang]
    except KeyError:
        return "N/A"
    
def get_country(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader, lang: str) -> str:
    try:
        countryModelRecord: geoip2.models.Country = get_country_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if countryModelRecord==None:
            return "N/A"
        else:
            return countryModelRecord.country.names[lang]
    except KeyError:
        return "N/A"

def get_city(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader, lang: str) -> str:
    try:
        cityModelRecord: geoip2.models.City = get_city_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if cityModelRecord==None:
            return "N/A"
        else:
            return cityModelRecord.city.names[lang]
    except KeyError:
        return "N/A"

def get_asn_autonomous_system_number(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader) -> int:
    try:
        asnModelRecord: geoip2.models.ASN = get_asn_geoip2_record(ip_address, geoip2Reader)
    except ValueError:
        return "N/A"
    
    try:
        if asnModelRecord==None:
            return "N/A"
        else:
            return asnModelRecord.autonomous_system_number
    except KeyError:
        return "N/A"

def get_asn_autonomous_system_organization(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader) -> str:
    try:
        asnModelRecord: geoip2.models.ASN = get_asn_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if asnModelRecord==None:
            return "N/A"
        else:
            return asnModelRecord.autonomous_system_organization
    except KeyError:
        return "N/A"

def get_latitude(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader):
    try:
        cityModelRecord: geoip2.models.City = get_city_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if cityModelRecord==None:
            return "N/A"
        else:
            return cityModelRecord.location.latitude 
    except KeyError:
        return "N/A"

def get_longitude(ip_address: geoip2.types.IPAddress, geoip2Reader: geoip2.database.Reader):
    try:
        cityModelRecord: geoip2.models.City = get_city_geoip2_record(ip_address, geoip2Reader)    
    except ValueError:
        return "N/A"
    
    try:
        if cityModelRecord==None:
            return "N/A"
        else:
            return cityModelRecord.location.longitude 
    except KeyError:
        return "N/A"

def generateCSVFromGeoIP2Module(dbPath, lang: str="en", inputCSVFileName: str="IP.csv", outputCSVFileName: str="IP_con_geoip.csv"):
    # Apri il file CSV con gli indirizzi IP
    try:
        with open(inputCSVFileName) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader) # Salta la prima riga con l'intestazione
            ip_list = [row[0] for row in csv_reader]
    except IOError:
        print(f"Errore durante l'apertura del file CSV '{inputCSVFileName}'")
        return

    try:
        # Scrivi i risultati su un nuovo file CSV utilizzando GeoIP2 DatabaseReader
        with open(outputCSVFileName, mode="w", newline="", encoding="utf-8") as csv_file:
            try:
                file_name = "GeoLite2-ASN.mmdb"
                file_path = os.path.join(dbPath, file_name)
                geoip2Reader_ASN = geoip2.database.Reader(file_path)
                file_name = "GeoLite2-City.mmdb"
                file_path = os.path.join(dbPath, file_name)
                geoip2Reader_City = geoip2.database.Reader(file_path)
                file_name = "GeoLite2-Country.mmdb"
                file_path = os.path.join(dbPath, file_name)
                geoip2Reader_Country = geoip2.database.Reader(file_path)
            except FileNotFoundError as e:
                print(f"{e}")
                sys.exit(1)
            # Crea una lista di tuple
            geoip2_list = [
            (
            ip_address
            , get_continent(ip_address, geoip2Reader_Country, lang)
            , get_country(ip_address, geoip2Reader_Country, lang)
            , get_city(ip_address, geoip2Reader_City, lang)
            , get_asn_autonomous_system_number(ip_address, geoip2Reader_ASN)
            , get_asn_autonomous_system_organization(ip_address, geoip2Reader_ASN)
            , get_latitude(ip_address, geoip2Reader_City)
            , get_longitude(ip_address, geoip2Reader_City)
            ) for ip_address in ip_list
            ]

            try:
                # Chiudi i Reader
                geoip2Reader_ASN.close()
                geoip2Reader_City.close()
                geoip2Reader_Country.close()
            except UnboundLocalError as e:
                print(f"{e}")
                sys.exit(1)

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
            for ip_address, continent, country, city, asn_autonomous_system_num, asn_autonomous_system_org, latitude, longitude in geoip2_list:
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
    except FileNotFoundError as e:
        print(f"{e}")