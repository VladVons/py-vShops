# Created: 2024.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from base64 import b64encode
from bs4 import BeautifulSoup
#
from Inc.DbList.DbUtil import DblToXlsx
from Inc.Scheme.Scheme import TSoupScheme
import IncP.LibCtrl as Lib


async def Main(self, aData: dict = None) -> dict:
    Url = Lib.DeepGetByList(aData, ['post', 'url'])
    if (Url):
        FileScheme = Lib.GetPkgFile(__package__, 'denis.ua.json')
        with open(FileScheme, 'r', encoding='utf8') as F:
            Scheme = json.load(F)

        UrlData = await Lib.TRequestGet().Send(Url)
        if ('err' not in UrlData):
            Soup = BeautifulSoup(UrlData['data'], 'lxml')
            SoupScheme = TSoupScheme()
            Parsed = SoupScheme.Parse(Soup, Scheme)
            DblData = Lib.DeepGetByList(Parsed, ['product', 'pipe', 'price'])

            Dbl = Lib.TDbList(['name', 'price_old', 'price_new'], DblData)
            Xlsx = DblToXlsx([Dbl])

            return {
                'dbl': Dbl.Export(),
                'file': b64encode(Xlsx),
                'url': Url
            }
