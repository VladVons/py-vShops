# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_ProductsRnd_LangImagePrice(self, aLang: str, aLimit: int = 24) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsRnd_LangImagePrice.sql',
        {'aLang': aLang, 'aLimit': aLimit}
    )

async def Get_Product_LangId(self, aLang: str, aProductId: int) -> dict:
    return await self.ExecQuery(
        'fmtGet_Product_LangId.sql',
        {'aLang': aLang, 'aProductId': aProductId}
    )


async def Get_Products_LangFilter(self, aLangId: int, aFilter: str, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    FilterRe = [f"('%{x}%')" for x in re.split(r'\s+', aFilter)]
    return await self.ExecQuery(
        'fmtGet_Products_LangFilter.sql',
        {'aLangId': aLangId, 'aFilter': aFilter, 'FilterRe': ', '.join(FilterRe), 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )

