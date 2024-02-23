# Created: 2024.02.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibModel import ListIntToComma


async def Get_TenantProducts_LangImagePrice(self, aLangId: int, aTenantId: int, aPriceId: int, aOrder: str, aLimit: int = 100, aOffset: int = 0) -> dict:
    return await self.ExecQuery(
        'fmtGet_TenantProducts_LangImagePrice.sql',
        {'aTenantId': aTenantId, 'aLangId': aLangId, 'aPriceId': aPriceId, 'aOrder': aOrder, 'aLimit': aLimit, 'aOffset': aOffset}
    )
