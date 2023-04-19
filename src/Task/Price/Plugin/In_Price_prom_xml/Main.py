# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://prom.ua/ua/c3498848-comel-ukrayina.html
# https://comel-it.com.ua/ua/about_us
# https://timedetector.comel-it.com/ukportals/Promua.xml


from Inc.Util.Str import ToInt, ToFloat, ToBool
from Inc.ParserX.Parser_xml import TParser_xml
from ..CommonDb import TDbCategory, TDbProductEx


class TCategory(TParser_xml):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCategory())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        Val = aRow.getAttribute('id')
        Rec.SetField('id', ToInt(Val))

        Val = aRow.getAttribute('parentId')
        Rec.SetField('parent_id', ToInt(Val))

        Val = aRow.firstChild.data
        Rec.SetField('name', Val)

        Rec.Flush()

class TProduct(TParser_xml):
    def __init__(self, aParent):
        super().__init__(aParent, TDbProductEx())

    def _Fill(self, aRow):
        Rec = self.Dbl.RecAdd()

        Val = aRow.getAttribute('id')
        Rec.SetField('id', ToInt(Val))

        Val = aRow.getElementsByTagName('categoryId')[0].firstChild.data
        Rec.SetField('category_id', ToInt(Val))

        Val = aRow.getElementsByTagName('name')[0].firstChild.data
        Rec.SetField('name', Val)

        Val = aRow.getElementsByTagName('vendorCode')[0].firstChild.data
        Rec.SetField('mpn', Val)

        Val = aRow.getElementsByTagName('price')[0].firstChild.data
        Rec.SetField('price', ToFloat(Val))

        Val = aRow.getElementsByTagName('available')[0].firstChild.data
        Rec.SetField('available', int(ToBool(Val)))

        Data = aRow.getElementsByTagName('vendor')
        if (Data):
            Rec.SetField('vendor', Data[0].firstChild.data)

        # Data = aRow.getElementsByTagName('description')[0].firstChild
        # if (Data):
        #    Val = Data.data
        #    Rec.SetField('descr', Val)

        Data = aRow.getElementsByTagName('image')
        Val = [x.firstChild.data for x in Data]
        Rec.SetField('image', Val)

        Data = aRow.getElementsByTagName('param')
        Val = {x.getAttribute('name'): x.firstChild.data for x in Data}
        Rec.SetField('feature', Val)

        Rec.Flush()
