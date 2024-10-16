# Created: 2024.02.09
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList, TDbRec
from Inc.Misc.Sitemap import TSitemap
from Inc.Var.Dict import DeepGetByList
from IncP.FormBase import TFormBase


class TSitemapProduct(TSitemap):
    def __init__(self, aDir: str, aUrlRoot: str, aParent):
        super().__init__(aDir, aUrlRoot)
        self.Parent = aParent

    async def _GetSize(self) -> int:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_product_count'
            }
        })
        return Data['count']

    async def _GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_product_data',
                'limit': aLimit,
                'offset': aOffset
            }
        })
        return TDbList().Import(Data)

    async def _GetRow(self, aRec: TDbRec) -> str:
        Res = [
            f'  <loc>{self.UrlRoot}{aRec.href}</loc>',
            f'  <lastmod>{aRec.update_date}</lastmod>'
        ]
        return '\n'.join(Res)


class TSitemapCategory(TSitemap):
    def __init__(self, aDir: str, aUrlRoot: str, aParent):
        super().__init__(aDir, aUrlRoot)
        self.Parent = aParent
        self.BaseName = 'sitemap_category'

    async def _GetSize(self) -> int:
        Dbl = await self._GetData(1, 0)
        if (Dbl):
            Res = Dbl.Rec.total
        else:
            Res = 0
        return Res

    async def _GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_categories_data',
                'limit': aLimit,
                'offset': aOffset
            }
        })
        return TDbList().Import(Data)

    async def _GetRow(self, aRec: TDbRec) -> str:
        Res = [
            f'  <loc>{self.UrlRoot}{aRec.href}</loc>'
        ]
        return '\n'.join(Res)

class TSitemapPages(TSitemap):
    def __init__(self, aDir: str, aUrlRoot: str, aParent):
        super().__init__(aDir, aUrlRoot)
        self.Parent = aParent
        self.BaseName = 'sitemap_pages'

    async def _GetSize(self) -> int:
        Dbl = await self._GetData(1, 0)
        if (Dbl):
            Res = Dbl.Rec.total
        else:
            Res = 0
        return Res

    async def _GetData(self, aLimit: int, aOffset: int) -> TDbList:
        Data = await self.Parent.ExecCtrl(self.Parent.out.route, {
            'method': 'ajax',
            'type': 'api',
            'param': {
                'method': 'get_pages_data',
                'limit': aLimit,
                'offset': aOffset
            }
        })
        return TDbList().Import(Data)

    async def _GetRow(self, aRec: TDbRec) -> str:
        Res = [
            f'  <loc>{self.UrlRoot}{aRec.href}</loc>'
        ]
        return '\n'.join(Res)

class TForm(TFormBase):
    async def _DoRender(self):
        Data = await self.ExecCtrlDef()
        self.out.update(Data)

        if (DeepGetByList(self.out, ['data', 'btn_submit']) is not None):
            Dir = 'MVC/catalog/view'
            Host = f'{self.Parent.Conf.request_scheme}://{self.Request.host}'

            SitemapPages = TSitemapPages(Dir, Host, self)
            ArrPages = await SitemapPages.CreateIndexes()

            SitemapCategory = TSitemapCategory(Dir, Host, self)
            ArrCategory = await SitemapCategory.CreateIndexes()

            SitemapProduct = TSitemapProduct(Dir, Host, self)
            ArrProduct = await SitemapProduct.CreateIndexes()
            ArrProduct.extend(ArrCategory)
            ArrProduct.extend(ArrPages)
            SitemapProduct.WriteIndexes(ArrProduct)

            self.out['in_process'] = 'ok'
