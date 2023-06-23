# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCrawl


class TCrawl(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCrawl())

    def _Fill(self, aRow: dict):
        if (not aRow.get('url')) or (not aRow.get('image1')):
            return

        Rec = self.Dbl.RecAdd()

        for x in ['code', 'url']:
            self.Copy(x, aRow, Rec)

        Images = [aRow.get(x) for x in ['image1', 'image2', 'image3'] if aRow.get(x)]
        Rec.SetField('image', Images)

        Rec.Flush()
