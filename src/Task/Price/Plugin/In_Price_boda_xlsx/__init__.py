# Created: 2023.11.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.ParserX.Common import TPluginBase
from IncP.Log import Log
from .Price import TPricePC, TPriceLaptop, TPriceMonit, TPricePrinter
from ..CommonDb import TDbCategory, TDbProductEx


class TIn_Price_boda_xlsx(TPluginBase):
    def ToDbProductEx(self, aParser, aDbProductEx: TDbProductEx, aCategoryId):
        for Rec in aParser.Dbl:
            aDbProductEx.RecAdd().SetAsDict({
                'category_id': aCategoryId,
                'code': Rec.code,
                'name': Rec.title,
                'price': Rec.price,
                'price_in': Rec.price_in,
                'qty': Rec.qty,
                'cond': Rec.cond,
                'attr': Rec.attr
            })

    async def Run(self):
        XTable = {
            'COMPUTERS': {
                'parser': TPricePC, 'category_id': 1, 'category': "Комп'ютер", 'enabled': True
            },
            'MONITORS': {
                'parser': TPriceMonit,'category_id': 2, 'category': 'Монітор'
            },
            'LAPTOPS': {
                'parser': TPriceLaptop, 'category_id': 3, 'category': 'Ноутбук'
            },
            'PRINTERS': {
                'parser': TPricePrinter, 'category_id': 4, 'category': 'Принтер'
            }
        }

        DbProductEx = TDbProductEx()
        DbCategory = TDbCategory()
        Engine = None
        Cached = False
        for xKey, xVal in XTable.items():
            if (xVal.get('enabled', True)) and (xKey in self.Conf['sheet']):
                Parser = xVal['parser'](self)
                if (Engine):
                    Parser.InitEngine(Engine)
                else:
                    Engine = Parser.InitEngine()
                Parser.SetSheet(xKey)
                await Parser.Load()
                Cached |= Parser.Cached
                self.ToDbProductEx(Parser, DbProductEx, xVal['category_id'])
                DbCategory.RecAdd().SetAsDict({'id': xVal['category_id'], 'parent_id': 0, 'name': xVal['category']})

        return {'cached': Cached, 'TDbCategory': DbCategory, 'TDbProductEx': DbProductEx}
