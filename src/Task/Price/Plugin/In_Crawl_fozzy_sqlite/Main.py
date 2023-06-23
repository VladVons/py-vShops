# Created: 2023.05.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_sqlite import TParser_sqlite
from ..CommonDb import TDbCrawl


class TMain(TParser_sqlite):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())

    def _Fill(self, aRow: dict):
        Rec = self.Dbl.RecAdd()

        Val = str(aRow['code'])
        Rec.SetField('code', Val)

        Val = aRow['images'].split(',')
        Rec.SetField('image', Val)

        Val = aRow['category']
        Rec.SetField('category', f'f1{Val}')

        for x in ['url', 'product', 'features', 'descr']:
            self.Copy(x, aRow, Rec)

        Rec.Flush()
