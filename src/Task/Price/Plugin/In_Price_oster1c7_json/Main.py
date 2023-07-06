# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Str import ToInt, ToFloat
from Inc.ParserX.Parser_xml import TParser_xml
from ..CommonDb import TDbCategory, TDbProductEx


class TCategory(TParser_xml):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCategory())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        Val = aRow.getAttribute('ID')
        Rec.SetField('id', ToInt(Val))

        Val = aRow.getAttribute('ParentID')
        Rec.SetField('parent_id', ToInt(Val))

        Val = aRow.firstChild.data
        Rec.SetField('name', Val)

        Rec.Flush()

class TProduct(TParser_xml):
    def __init__(self, aParent):
        super().__init__(aParent, TDbProductEx())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        Val = aRow.getElementsByTagName('Code')[0].firstChild.data
        Rec.SetField('id', ToInt(Val))

        Val = aRow.getElementsByTagName('Articul')[0].firstChild
        if (Val is not None):
            Rec.SetField('barcode', Val.data)

        Val = aRow.getElementsByTagName('CategoryID')[0].firstChild.data
        Rec.SetField('category_id', ToInt(Val))

        Val = aRow.getElementsByTagName('Name')[0].firstChild.data
        Rec.SetField('name', Val)

        Val = aRow.getElementsByTagName('PriceOut')[0].firstChild.data
        Rec.SetField('price', ToFloat(Val))

        Val = aRow.getElementsByTagName('Quantity')[0].firstChild.data
        Rec.SetField('qty', Val)

        Val = aRow.getElementsByTagName('Descr')[0].firstChild
        if (Val is not None):
            Rec.SetField('descr', Val.data)

        Val = aRow.getElementsByTagName('Image')[0].firstChild
        if (Val is not None):
            Rec.SetField('image', [Val.data])

        Rec.Flush()
