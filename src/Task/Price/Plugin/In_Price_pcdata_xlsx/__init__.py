# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://pc-data.com.pl
# https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit
# https://docs.google.com/spreadsheets/d/1c4HxmK5XUi0FzwdzFleFAVL02-UTRdIvEpaPwwV2yKo/edit (boda)


import os
#
from Inc.ParserX.Common import TPluginBase
from IncP.Log import Log
from .Price import TPricePC, TPriceNotebook, TPriceMonit, TPriceMonitInd, TPricePrinter
from ..CommonDb import TDbCategory, TDbProductEx


class TIn_Price_pcdata_xlsx(TPluginBase):
    def ToDbProductEx(self, aParser, aDbProductEx: TDbProductEx, aCategoryId):
        Uniq = {}
        Price = 'price'
        PriceIn = 'price_in'

        Fields =  aParser.Dbl.GetFields()
        Fields.remove(Price)
        Fields.remove('attr')

        TitleToAttr = aParser.Dbl.ExportPair('title', 'attr')
        Dbl = aParser.Dbl.Group(Fields, [Price, PriceIn])
        for Rec in Dbl:
            Title = Rec.title
            if (Title in Uniq):
                Log.Print(1, 'i', f'Not unique title: {Title}')
            else:
                Uniq[Title] = ''
                PriceAvg = round(Rec.GetField(Price) / Rec.count, 1)
                Rec.SetField(Price, PriceAvg)
                PriceInAvg = round(Rec.GetField(PriceIn) / Rec.count, 1)
                Rec.SetField(PriceIn, PriceInAvg)

                aDbProductEx.RecAdd().SetAsDict({
                    'category_id': aCategoryId,
                    'code': Rec.code,
                    'name': Rec.title,
                    'price': PriceAvg,
                    'price_in': PriceInAvg,
                    'qty': Rec.count,
                    'cond': Rec.cond,
                    'attr': TitleToAttr[Rec.title]
                    })

    def GetHandlers(self) -> dict:
        return {
            'COMPUTERS': {
                'parser': TPricePC, 'category_id': 1, 'category': "Комп'ютер"
            },
            'MONITORS': {
                'parser': TPriceMonit,'category_id': 2, 'category': 'Монітор'
            },
            'INDUSTRIAL MONITORS': {
                'parser': TPriceMonitInd, 'category_id': 3, 'category': 'Монітор індустрійний'
            },
            'PRINTERS': {
                'parser': TPricePrinter, 'category_id': 4, 'category': 'Принтер'
            },
            'ALL IN ONES': {
                'parser': TPriceNotebook, 'category_id': 5, 'category': "Моноблок"
            },
            'LAPTOPS': {
                'parser': TPriceNotebook, 'category_id': 6, 'category': "Ноутбук", "enabled": False
            }
        }

    async def Run(self):
        DbProductEx = TDbProductEx()
        DbCategory = TDbCategory()
        Engine = None
        Cached = False
        for xKey, xVal in self.GetHandlers().items():
            if (xVal.get('enabled', True)):
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
