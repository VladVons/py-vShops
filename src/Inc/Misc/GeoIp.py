# Created: 2024.03.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# download database files from Git into /usr/share/GeoLite2
# https://github.com/P3TERX/GeoLite.mmdb?tab=readme-ov-file


import os
#
from geoip2.database import Reader


class TGeoIp():
    def __init__(self, aPath: str = None):
        self.aPath = aPath or '/usr/share/GeoLite2'
        assert(os.path.isdir(self.aPath)), f'Directory not exists {self.aPath}'

    def GetCity(self, aIp: str) -> dict:
        File = f'{self.aPath}/GeoLite2-City.mmdb'
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
