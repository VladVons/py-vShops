# Created: 2023.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from IncP.LibCtrl import DeepGetByList, Filter


async def RegSession(self, aData: dict) -> dict:
    return await self.ExecModel('system', Filter(aData, ['method', 'param']))

async def OnExec(self, aData: dict) -> dict:
    await self.Cache.ProxyA('conf_tenant_0', {}, self.GetConf, [aData])

    SessionId = DeepGetByList(aData, ['session', 'session_id'])
    if (SessionId):
        await self.ExecModel(
            'system',
            {
                'method': 'Ins_HistPageView',
                'param': {
                    'aSessionId': SessionId,
                    'aUrl': aData['path_qs']
                }
            }
        )
