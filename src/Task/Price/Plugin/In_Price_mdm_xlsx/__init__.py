# Created: 2023.07.05
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://www.mdmkomputery.pl/


import os
#
from Inc.ParserX.Common import TPluginBase
from .Price import TPricePC, TPriceMonit, TPriceNotebook
from ..CommonDb import TDbCategory, TDbProductEx


class TIn_Price_mdm_xlsx(TPluginBase):
    def ToDbProductEx(self, aParser, aDbProductEx: TDbProductEx, aCategoryId):
        FieldAvg = 'price'
        Fields =  aParser.Dbl.GetFields()
        Fields.remove(FieldAvg)
        Dbl = aParser.Dbl.Group(Fields, [FieldAvg])
        for Rec in Dbl:
            Avg = round(Rec.GetField(FieldAvg) / Rec.count, 1)
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()

            aDbProductEx.RecAdd().SetAsDict({
                'category_id': aCategoryId,
                'code': Rec.code,
                'name': Rec.title,
                'price': Avg,
                'qty': Rec.count
                })
        aDbProductEx.Sort(['code'])

    async def Run(self):
        XTable = {
            'Desktops': {
                'parser': TPricePC, 'category_id': 1, 'category': 'Компютер'
            },
            'Monitors': {
                'parser': TPriceMonit,'category_id': 2, 'category': 'Монітор', 'enable': not False
            },
            'Laptopy': {
                'parser': TPriceNotebook,'category_id': 3, 'category': 'Ноутбук',
            }
        }

        DbProductEx = TDbProductEx()
        DbCategory = TDbCategory()
        Engine = None
        for xKey, xVal in XTable.items():
            if (xVal.get('enable', True)):
                Parser = xVal['parser'](self)
                if (Engine):
                    Parser.InitEngine(Engine)
                else:
                    Engine = Parser.InitEngine()
                Parser.SetSheet(xKey)
                await Parser.Load()
                self.ToDbProductEx(Parser, DbProductEx, xVal['category_id'])
                DbCategory.RecAdd().SetAsDict({'id': xVal['category_id'], 'parent_id': 0, 'name': xVal['category']})

        return {'TDbCategory': DbCategory, 'TDbProductEx': DbProductEx}
