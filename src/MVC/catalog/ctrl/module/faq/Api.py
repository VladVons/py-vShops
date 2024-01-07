# Created: 2023.12.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList


async def Main(self, aData: dict = None) -> dict:
    aModuleId = DeepGetByList(aData, ['rec', 'id'])
    LangId = self.GetLangId('ua')

    Dbl = await self.ExecModelImport(
        'system',
        {
            'method': 'Get_ModuleLang',
            'param': {
                'aLangId': LangId,
                'aModuleId': aModuleId
            }
        }
    )
    if (Dbl):
        return {
            'dbl_faq': Dbl.Export()
        }
