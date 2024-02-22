# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://pc-data.com.pl
# https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit
# https://docs.google.com/spreadsheets/d/1c4HxmK5XUi0FzwdzFleFAVL02-UTRdIvEpaPwwV2yKo/edit (boda)


import os
import gspread
#
from Inc.ParserX.Common import TPluginBase
from IncP.Log import Log
from .Price import TPricePC, TPriceMonit, TPriceMonitInd, TPricePrinter
from ..CommonDb import TDbCategory, TDbProductEx


class TIn_Price_pcdata_xlsx(TPluginBase):
    def Download(self, aUrl: str, aFile: str) -> bool:
        AuthFile = os.path.expanduser('~/.config/gspread/service_account.json')
        assert(os.path.isfile(AuthFile)), f'File does not exist {AuthFile}'

        GSA = gspread.service_account()
        SH = GSA.open_by_url(aUrl)
        Data = SH.export(format = gspread.utils.ExportFormat.EXCEL)
        with open(aFile, 'wb') as F:
            F.write(Data)
            return True

    def ToDbProductEx(self, aParser, aDbProductEx: TDbProductEx, aCategoryId):
        Uniq = {}
        Price = 'price'
        PriceIn = 'price_in'
        Fields =  aParser.Dbl.GetFields()
        Fields.remove(Price)
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
                    'used': Rec.used
                    })

    async def Run(self):
        Url = self.Conf.GetKey('url_gspread')
        if (Url):
            File = self.GetFile()
            if (not os.path.isfile(File)):
                self.Download(Url, File)

        XTable = {
            'COMPUTERS': {
                'parser': TPricePC, 'category_id': 1, 'category': "Комп'ютер", "enabled": True
            },
            'MONITORS': {
                'parser': TPriceMonit,'category_id': 2, 'category': 'Монітор'
            },
            'INDUSTRIAL MONITORS': {
                'parser': TPriceMonitInd, 'category_id': 3, 'category': 'Монітор індустрійний'
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
