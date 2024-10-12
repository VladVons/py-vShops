# Created: 2024.08.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from datetime import datetime
from base64 import b64encode
from Inc.DbList.DbConvert import DblToXlsx
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

        FieldsFmt = {
            'category': {'name': Lib.ResGetLang(aQuery, 'category')},
            'id':       {'name': Lib.ResGetLang(aQuery, 'id')},
            'product':  {'name': Lib.ResGetLang(aQuery, 'product'), 'width': 60},
            'rest':     {'name': Lib.ResGetLang(aQuery, 'rest'), 'width': 5},
            'price':    {'name': Lib.ResGetLang(aQuery, 'price'), 'format': '#0'}
        }

        DblList = []
        Category = ''
        Fields = Dbl.GetFields()
        for Rec in Dbl:
            if (Category != Rec.category):
                Category = Rec.category
                DblNew = Lib.TDbList(Fields)
                DblNew.Tag = {
                    'name': Category,
                    'fields': FieldsFmt
                }
                DblList.append(DblNew)

            DblNew.RecAdd(list(Rec.Data))
            DblNew.Rec.rest = Lib.HideDigit(DblNew.Rec.rest)

        DblNew = Lib.TDbList(
            ['name', 'value'],
            [
                ['date', datetime.now().strftime('%Y-%m-%d')],
                ['url', Lib.ResGetLang(aQuery, 'url_')],
                ['address', Lib.ResGetLang(aQuery, 'address_')],
                ['phone', Lib.ResGetLang(aQuery, 'phone1_')],
                ['phone', Lib.ResGetLang(aQuery, 'phone2_')]
            ]
        )
        DblNew.Tag = {'name': Lib.ResGetLang(aQuery, 'info')}
        DblList.append(DblNew)

        Xlsx = DblToXlsx(DblList)
        return {'file': b64encode(Xlsx)}
