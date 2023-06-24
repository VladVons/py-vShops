# Created: 2023.06.22
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCrawl


class TMain(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())

    def _Fill(self, aRow: dict):
        aCode = aRow.get('code')
        if (aCode):
            aCode = str(aCode).strip()
            if (len(aCode) >= 4):
                Rec = self.Dbl.RecAdd()
                for x in ['tenant', 'category', 'code', 'model', 'url']:
                    self.Copy(x, aRow, Rec)

                Rec.Flush()
