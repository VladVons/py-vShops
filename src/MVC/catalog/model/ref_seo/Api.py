# Created: 2024.03.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_SeoToDict(self, aPath: list[str]) -> dict:
    Arr = [f"(keyword = '{x}' or keyword like '%/{x}')" for x in aPath]
    CondKeyword = ' or\n'.join(Arr)
    return await self.ExecQuery(
        'fmtGet_SeoToDict.sql',
        {'CondKeyword': CondKeyword}
    )

async def Get_SeoFromDict(self, aData: list) -> dict:
    Data = [f"('{Key}', '{Val}', {Idx})" for Key, Val, Idx in aData]
    return await self.ExecQuery(
        'fmtGet_SeoFromDict.sql',
        {'Data': ', '.join(Data)}
    )

async def Set_SeoProducts(self) -> dict:
    return await self.ExecQuery(
        'fmtSet_SeoProducts.sql',
        {}
    )
