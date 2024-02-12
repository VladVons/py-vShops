# Created: 2023.07.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DbList import TDbList, TDbRec


class TSitemap():
    def __init__(self, aDir: str, aUrlRoot: str):
        self.Dir = aDir
        self.UrlRoot = aUrlRoot
        self.MaxRowsRead = 1000
        self.MaxRowsWrite = 49999 # max records in file
        self.Size = 0
        self.BaseName = 'sitemap'

    async def _GetSize(self) -> int:
        raise NotImplementedError()

    async def _GetData(self, aLimit: int, aOffset: int) -> TDbList:
        raise NotImplementedError()

    async def _GetRow(self, aRec: TDbRec) -> str:
        raise NotImplementedError()

    def _WriteFile(self, aFile: str, aData: str):
        with open(f'{self.Dir}/{aFile}', 'w', encoding='utf8') as F:
            F.write(aData)

    async def WriteIndex(self, aFile: str, aOffset: int = 0) -> int:
        Res = 0
        Offset = 0
        MaxRows = min(self.MaxRowsRead, self.MaxRowsWrite)

        Arr = []
        Arr.append('<?xml version="1.0" encoding="UTF-8"?>')
        Arr.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        while True:
            Dbl = await self._GetData(MaxRows, aOffset + Offset)
            if (Dbl.IsEmpty()):
                break

            for Rec in Dbl:
                RowData = await self._GetRow(Rec)

                Arr.append('  <url>')
                Arr.append(RowData)
                Arr.append('  </url>')

            Offset += Dbl.GetSize()
            if (Offset >= self.MaxRowsWrite):
                Res = aOffset + Offset
                break
        Arr.append('</urlset>')
        self._WriteFile(aFile, '\n'.join(Arr))
        return Res

    async def CreateIndexes(self) -> list:
        Idx = 0
        Res = []
        Offset = 0
        while True:
            Idx += 1
            File = f'{self.BaseName}_{Idx}.xml'

            Res.append('  <sitemap>')
            Res.append(f'    <loc>{self.UrlRoot}/{File}</loc>')
            Res.append('  </sitemap>')

            Offset = await self.WriteIndex(File, Offset)
            if (not Offset):
                break
        return Res

    def WriteIndexes(self, aData: list):
        Arr = []
        Arr.append('<?xml version="1.0" encoding="UTF-8"?>')
        Arr.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
        Arr.extend(aData)
        Arr.append('</sitemapindex>')
        self._WriteFile(f'{self.BaseName}.xml', '\n'.join(Arr))

    async def Create(self):
        self.Size = await self.GetSize()
        if (self.Size > self.MaxRowsWrite):
            Arr = await self.CreateIndex()
            self.WriteIndexes(Arr)
        else:
            await self.WriteIndex(f'{self.BaseName}.xml')
