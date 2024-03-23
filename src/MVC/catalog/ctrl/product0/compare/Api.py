# Created: 2024.03.06
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDefs, IsDigits, TDbList
from ..._inc.products_a import Main as products_a

async def Main(self, aData: dict = None) -> dict:
    aProductIds, aLang  = GetDictDefs(
        aData.get('query'),
        ('product_ids', 'lang'),
        ('', 'ua')
    )

    ProductIds = aProductIds.strip('[]').split(';')
    if (not IsDigits(ProductIds)):
        return {'status_code': 404}

    aLangId = self.GetLangId(aLang)
    Dbl = await self.ExecModelImport(
        'ref_product0/product',
        {
            'method': 'Get_ProductsAttr',
            'param': {
                'aLangId': aLangId,
                'aProductIds': ProductIds
            }
        }
    )
    if (not Dbl):
        return {'status_code': 404}

    Attrs = []
    for Rec in Dbl:
        if (Rec.attr):
            Attrs += Rec.attr.keys()
    AttrEx = ['image', 'product_id', 'product_title', 'price', 'category_id', 'category_title', 'tenant_id']
    Attrs = AttrEx + sorted(set(Attrs))

    DblCompare = TDbList(Attrs)
    for Rec in Dbl:
        RecNew = DblCompare.RecAdd()
        for x in AttrEx:
            RecNew.SetField(x, Rec.GetField(x))

        Items = Rec.GetField('attr', {}).items()
        for Key, Val in Items:
            RecNew.SetField(Key, Val)

    DblCompare = await products_a(self, DblCompare)

    ToHide = ['image', 'product_id', 'category_id', 'category_title', 'tenant_id', 'product_href', 'category_href', 'tenant_href']
    DblCompare.Rec.RenameFields(ToHide, [f'_{x}'for x in ToHide])

    Res = {
        'dbl_compare': DblCompare.Export(),
        'rows': [x for x in DblCompare.GetFields() if (not x.startswith('_'))]
    }
    return Res
