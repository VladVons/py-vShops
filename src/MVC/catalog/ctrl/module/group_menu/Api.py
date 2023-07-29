# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import TDbSql, DeepGetByList


async def Main(self, aData: dict = None) -> dict:
    aLang = DeepGetByList(aData, ['query', 'lang'], 'ua')
    ModuleId = aData['rec']['id']
    Res = await self.ExecModel(
        'system',
        {
            'method': 'Get_ModuleGroup',
            'param': {'aLang': aLang, 'aModuleId': ModuleId}
        }
    )
    Res.update(aData['rec'])

    DblData = Res.get('data')
    if (DblData):
        Href = []
        Dbl = TDbSql().Import(DblData)
        for Rec in Dbl:
            Route = Rec.GetField('route', 'information/information')
            Href.append(f'?route={Route}&module_id={Rec.id}')
        Dbl.AddFields(['href'], [Href])
        Res['data'] = Dbl.Export()
    return Res
