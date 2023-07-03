# Created: 2023.07.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList, TDbRec


class TSitemap():
    def __init__(self, aDir: str, aUrlRoot: str, aMaxRows: int):
        self.Dir = aDir
        self.UrlRoot = aUrlRoot
        self.MaxRowsRead = aMaxRows
        self.MaxRowsWrite = 50000

    async def GetSize(self) -> int:
        raise NotImplementedError()

    async def GetData(self, aLimit: int, aOffset: int) -> TDbList:
        raise NotImplementedError()

    async def GetRow(self, aRec: TDbRec) -> str:
        raise NotImplementedError()

    def FileWrite(self, aFile: str, aData: str):
        with open(f'{self.Dir}/{aFile}', 'w', encoding='utf8') as F:
            F.write(aData)

    async def CreateFile(self, aFile: str, aOffset: int = 0) -> int:
        Res = 0
        Offset = 0
        MaxRows = min(self.MaxRowsRead, self.MaxRowsWrite)

        Arr = []
        Arr.append('<?xml version="1.0" encoding="UTF-8"?>')
        Arr.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        while True:
            Dbl = await self.GetData(MaxRows, aOffset + Offset)
            if (Dbl.IsEmpty()):
                break

            for Rec in Dbl:
                Loc = await self.GetRow(Rec)

                Arr.append('  <url>')
                Arr.append(f'  <loc>{self.UrlRoot}/{Loc}</loc>')
                Arr.append('  </url>')

            Offset += Dbl.GetSize()
            if (Offset >= self.MaxRowsWrite):
                Res = aOffset + Offset
                break
        Arr.append('</urlset>')
        self.FileWrite(aFile, '\n'.join(Arr))
        return Res

    async def CreateIndex(self):
        Idx = 0
        Arr = []
        Arr.append('<?xml version="1.0" encoding="UTF-8"?>')
        Arr.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        Offset = 0
        while True:
            Idx += 1
            File = f'sitemap_{Idx}.xml'

            Arr.append('  <sitemap>')
            Arr.append(f'    <loc>{self.UrlRoot}/{File}</loc>')
            Arr.append('  </sitemap>')

            Offset = await self.CreateFile(File, Offset)
            if (not Offset):
                break
        Arr.append('</sitemapindex>')
        self.FileWrite('sitemap.xml', '\n'.join(Arr))

    async def Create(self):
        Size = await self.GetSize()
        if (Size > self.MaxRowsWrite):
            await self.CreateIndex()
        else:
            await self.CreateFile('sitemap.xml')
