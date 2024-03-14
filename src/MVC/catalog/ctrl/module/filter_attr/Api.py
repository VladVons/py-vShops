# Created: 2024.03.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import Replace


def AttrEncode(aItems: list) -> str:
    Attr = {}
    for xItem in aItems:
        AttrId, Val, _ValMax = xItem
        if (AttrId not in Attr):
            Attr[AttrId] = ''
        Attr[AttrId] += Val + ';'

    Res = [f'{Key}:{Val};' for Key, Val in Attr.items()]
    return ''.join(Res)


async def Main(self, aData: dict = None) -> dict:
    Dbl = await self.ExecModelImport(
        'ref_attr',
        {
            'method': 'Get_AttrFilter',
            'param': {}
        }
    )

    if (Dbl):
        Dbl.AddFieldsFill(['href'], False)
        for Rec in Dbl:
            Attr = AttrEncode(Rec.filter)
            Attr = Replace(Attr, {"'": '&#39;', '"': '&quot;'})
            New = [
                f'/?route=product0/category&category_id={Rec.category_id}&attr=[{Attr}]'
            ]
            Dbl.RecMerge(New)

        Res = {
            'dbl_filter_attr': Dbl.Export()
        }
        return Res
