# Created: 2024.08.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from base64 import b64encode
from Inc.DbList.DbUtil import DblToXlsx
#
import IncP.LibCtrl as Lib

async def Main(self, aQuery: dict = None) -> dict:

    if (Lib.DeepGetByList(aQuery, ['post', 'btn_download'])):
        aLangId = self.GetLangId('ua')
        Dbl = await self.ExecModelImport(
            'ref_product0/product',
            {
                'method': 'Get_Products_PriceList',
                'param': {'aLangId': aLangId}
            }
        )

        Xlsx = DblToXlsx([Dbl])
        return {'file': b64encode(Xlsx)}
