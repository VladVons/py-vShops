# Created: 2023.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Str import ToFloat
from Inc.ParserX.Parser_xls import TParser_xls
from ..CommonDb import TDbCrawl


class TMain(TParser_xls):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())


    def _Fill(self, aRow: dict):
        Ean = aRow.get('ean')
        if (Ean):
            if (',' in Ean):
                Ean = Ean.split(',')[0]

            Rec = self.Dbl.RecAdd()

            Rec.SetField('ean', Ean)

            for x in ['category', 'product']:
                self.Copy(x, aRow, Rec)

            Rec.Flush()
