# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Parser_dbl import TParser_dbl
from ..CommonDb import TDbCategory, TDbProductEx


class TCategory(TParser_dbl):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCategory())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        for x in ['id', 'parent_id', 'name']:
            self.Copy(x, aRow, Rec)

        Rec.Flush()

class TProduct(TParser_dbl):
    def __init__(self, aParent):
        super().__init__(aParent, TDbProductEx())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        Val = aRow['product_id']
        Rec.SetField('id', Val)

        Val = aRow['ean']
        Rec.SetField('code', Val)

        for x in ['category_id', 'name', 'qty', 'price']:
            self.Copy(x, aRow, Rec)

        Rec.Flush()
