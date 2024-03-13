from geoip2.database import Reader


Ip = '5.58.6.236'
Ip = '46.173.175.14'
Ip = '8.8.8.8'

def Test1():
    with Reader('/usr/share/GeoLite2/GeoLite2-ASN.mmdb') as reader:
        response = reader.asn(Ip)
        print(response.autonomous_system_number)
        print(response.autonomous_system_organization)

def Test2():
    with Reader('/usr/share/GeoLite2/GeoLite2-City.mmdb') as reader:
        response = reader.city(Ip)
        Res = {'country': response.country.name, 'city': response.city.name}

        print("City Name:", response.city.name)
        print("Country Code:", response.country.iso_code)
        print("Country Name:", response.country.name)
        print("Continent Code:", response.continent.code)
        print("Continent Name:", response.continent.name)
        print("Latitude:", response.location.latitude)
        print("Longitude:", response.location.longitude)

Test2()
pass
