# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, DeepGetByList


async def Main(self, aData: dict = None) -> dict:
    aLangId = DeepGetByList(aData, ['query', 'lang'], 1)
    ModuleId = aData['rec']['id']
    Res = await self.ExecModel(
        'system',
        {
            'method': 'Get_ModuleGroup',
            'param': {'aLangId': aLangId, 'aModuleId': ModuleId}
        }
    )
    Res.update(aData['rec'])

    Href = []
    Dbl = TDbSql().Import(Res.get('data'))
    for Rec in Dbl:
        Href.append(f'information/information&path={Rec.id}')
    Dbl.AddFields(['href'], [Href])
    Res['data'] = Dbl.Export()
    return Res
