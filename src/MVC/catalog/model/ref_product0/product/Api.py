# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


async def Get_ProductsRnd_LangImagePrice(self, aLang: str, aLimit: int = 24) -> dict:
    return await self.ExecQuery(
        'fmtGet_ProductsRnd_LangImagePrice.sql',
        {'aLang': aLang, 'aLimit': aLimit}
    )