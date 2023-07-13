# Created: 2023.05.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_csv import TParser_csv
from ..CommonDb import TDbCrawl


class TMain(TParser_csv):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())

    def _Fill(self, aRow: dict):
        if (aRow.get('code')):
            Rec = self.Dbl.RecAdd()
            self.Copy('code', aRow, Rec)
            Rec.Flush()
