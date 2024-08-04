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

        DblList = []
        Category = ''
        Fields = Dbl.GetFields()
        for Rec in Dbl:
            if (Category != Rec.category):
                Category = Rec.category
                DblNew = Lib.TDbList(Fields)
                DblNew.Tag = {
                    'name': Category,
                    'fields': {
                        'product': {'width': 60},
                        'rest': {'width': 5}
                    }
                }
                DblList.append(DblNew)

            DblNew.RecAdd(list(Rec.Data))
            Val = DblNew.Rec.rest
            if (Val > 10):
                Val = '>10'
            elif (Val > 5):
                Val = '>5'
            elif (Val > 1):
                Val = '>1'
            else:
                Val = '1'
            DblNew.Rec.rest = Val

        Xlsx = DblToXlsx(DblList)
        return {'file': b64encode(Xlsx)}
