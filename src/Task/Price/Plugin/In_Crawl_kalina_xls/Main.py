# Created: 2023.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_xls import TParser_xls
from Inc.Ean import TEan
from IncP.Log import Log
from ..CommonDb import TDbCrawl


class TMain(TParser_xls):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())


    def _Fill(self, aRow: dict):
        aEan = aRow.get('code')
        if (not aEan):
            return

        if (',' in aEan):
            aEan = aEan.split(',')[0]

        Ean = TEan()
        if (not Ean.Init(aEan).Check()):
            Log.Print(1, 'i', f'EAN error {aEan}')
            return

        Rec = self.Dbl.RecAdd()

        Rec.SetField('code', aEan)

        for x in ['category', 'product']:
            self.Copy(x, aRow, Rec)

        Rec.Flush()
