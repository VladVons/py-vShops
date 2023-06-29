# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit


import os
import gspread
#
from Inc.ParserX.Common import TPluginBase
from .Price import TPricePC, TPriceMonit, TPriceMonitInd
from ..CommonDb import TDbCategory, TDbProductEx


class TIn_Price_pl01_xlsx(TPluginBase):
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
                'model': Rec.code,
                'name': Rec.title,
                'price': Avg,
                'available': Rec.count
                })
        #Dbl.Sort(['model', 'screen'])

    async def Run(self):
        Url = self.Conf.GetKey('url_gspread')
        if (Url):
            File = self.GetFile()
            if (not os.path.isfile(File)):
                self.Download(Url, File)

        XTable = {
            'COMPUTERS': {
                'parser': TPricePC, 'category_id': 1, 'category': 'Компютер'
            },
            'MONITORS': {
                'parser': TPriceMonit,'category_id': 2, 'category': 'Монітор'
            },
            'INDUSTRIAL MONITORS': {
                'parser': TPriceMonitInd, 'category_id': 3, 'category': 'Монітор індустрійний'
            }
        }

        DbProductEx = TDbProductEx()
        DbCategory = TDbCategory()
        Engine = None
        for xKey, xVal in XTable.items():
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
