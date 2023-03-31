# Created: 2023.03.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import GetDictDef, TDbSql


async def Main(self, aData: dict = None) -> dict:
    _aTenantId, aLangId = GetDictDef(aData.get('query'), ('tenant', 'lang'), (0, 1))
    GroupId = aData['rec']['id']
    Res = await self.ExecModel(
        'system',
        {
            'method': 'Get_ModuleGroup',
            'param': {'aGroupId': GroupId, 'aLangId': aLangId}
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
