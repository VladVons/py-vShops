# Created: 2024.03.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import IncP.LibCtrl as Lib


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
    return

    Dbl = await self.ExecModelImport(
        'ref_attr',
        {
            'method': 'Get_AttrFilter',
            'param': {}
        }
    )

    if (Dbl):
        Hrefs = []
        for Rec in Dbl:
            Attr = Lib.HtmlEsc(AttrEncode(Rec.filter))
            Hrefs.append(f'/?route=product0/category&category_id={Rec.category_id}&attr=[{Attr}]')
        # ToDo
        #if (self.ApiCtrl.Conf.get('seo_url')):
        #    Hrefs = await SeoEncodeList(self, Hrefs)

        Dbl.AddFieldsFill(['href'], False)
        for Idx, Rec in enumerate(Dbl):
            Dbl.RecMerge([Hrefs[Idx]])

        Res = {
            'dbl_filter_attr': Dbl.Export()
        }
        return Res
