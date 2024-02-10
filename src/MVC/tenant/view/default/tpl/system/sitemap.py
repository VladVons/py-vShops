# Created: 2024.02.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList, TDbRec
from Inc.Misc.Sitemap import TSitemap
from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase


class TSitemapEx(TSitemap):
    def __init__(self, aDir: str, aUrlRoot: str, aParent):
        super().__init__(aDir, aUrlRoot)
        self.Parent = aParent

    async def GetSize(self) -> int:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_count'
            }
        })
        return Data['count']

    async def GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_data',
                'limit': aLimit,
                'offset': aOffset
            }
        })
        return TDbList().Import(Data)

    async def GetRow(self, aRec: TDbRec) -> str:
        Res = [
            f'  <loc>{self.UrlRoot}/?route=product0/product&product_id={aRec.id}</loc>',
            f'  <lastmod>{aRec.update_date}</lastmod>'
        ]
        return '\n'.join(Res)


class TForm(TFormBase):
    async def _DoRender(self):
        if (DeepGetByList(self.out, ['data', 'btn_sitemap']) is not None):
            Host = f'{self.Request.scheme}://{self.Request.host}'
            Sitemap = TSitemapEx('MVC/catalog/view/sitemap', Host, self)
            await Sitemap.Create()

        Data = await self.ExecCtrlDef()
        self.out.update(Data)

