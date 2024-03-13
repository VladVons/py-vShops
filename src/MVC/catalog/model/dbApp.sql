create or replace function check_ean(a_code text) returns boolean
as $$
    def GetCrc(aCode: str) -> int:
        Body = aCode[:-1]
        Data = [(3, 1)[i % 2] * int(x) for i, x in enumerate(reversed(Body))]
        return (10 - sum(Data)) % 10

    def CheckEan(aCode: str) -> bool:
        return  (8 <= len(aCode) <= 14) and \
                (aCode.isdigit()) and \
                (aCode[-1] == str(GetCrc(aCode)))

    return CheckEan(a_code)
$$ language plpython3u;

create or replace function geoip(a_ip text) returns jsonb
as $$
    from geoip2.database import Reader

    File = '/usr/share/GeoLite2/GeoLite2-City.mmdb'
    with Reader(File) as R:
        try:
            Data = R.city(aIp)
            Res = {
                'continent': Data.continent.name,
                'country': Data.country.name,
                'city': Data.city.name
            }
        except Exception as _E:
            Res = {}
    return Res
$$ language plpython3u;

create or replace function crypt_simple(a_text text, a_key int) returns text
as $$
    def CryptSimple(aText: str, aKey: int) -> str:
        '''
        aText: string to crypt
        aKey: positive value to crypt, negativ value to uncrypt
        '''

        def _Shift(aVal: str, aKey: int) -> str:
            aKey %= len(aVal)
            return aVal[aKey:] + aVal[:aKey]

        LenText = len(aText)
        if (LenText == 0):
            return aText

        LenNum = ord('9') - ord('0') + 1
        LenLat = ord('z') - ord('a') + 1
        LenCyr = ord('я') - ord('а') + 1
        aKey = aKey + LenText if (aKey > 0) else aKey - LenText

        Arr = []
        for x in aText:
            if ('0' <= x <= '9'):
                Base = ord('0')
                Len = LenNum
            elif ('a' <= x <= 'z'):
                Base = ord('a')
                Len = LenLat
            elif ('A' <= x <= 'Z'):
                Base = ord('A')
                Len = LenLat
            elif ('а' <= x <= 'я'):
                Base = ord('а')
                Len = LenCyr
            elif ('А' <= x <= 'Я'):
                Base = ord('А')
                Len = LenCyr
            else:
                Arr.append(x)
                continue

            x = chr((ord(x) - Base + aKey) % Len + Base)
            Arr.append(x)

        Res = ''.join(Arr)
        return _Shift(Res, LenText * 3)

    return CryptSimple(a_text, a_key)
$$ language plpython3u;
