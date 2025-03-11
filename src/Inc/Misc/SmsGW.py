# Created: 2025.03.11
# Author: Vladimir Vons <VladVons@gmail.com>
#
# https://github.com/capcom6/android-sms-gateway?tab=readme-ov-file#local-server


from base64 import b64encode
import aiohttp


class TSmsGW():
    def __init__(self, aUrl: str, aUser: str, aPassw: str):
        self.Url = aUrl

        Auth = b64encode(f'{aUser}:{aPassw}'.encode()).decode()
        self.HeadersAuth = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {Auth}'
        }

    @staticmethod
    async def _Result(aResponse) -> dict:
        if (aResponse.status in (200, 202)):
            Data = await aResponse.json()
            Res = {'status': aResponse.status, 'data': Data}
        else:
            Res = {'status': aResponse.status}
        return Res

    async def _Post(self, aUrl: str, aData: dict) -> dict:
        async with aiohttp.ClientSession() as Session:
            async with Session.post(aUrl, json=aData, headers=self.HeadersAuth) as Response:
                return await self._Result(Response)

    async def _Get(self, aUrl: str) -> dict:
        async with aiohttp.ClientSession() as Session:
            async with Session.get(aUrl, headers=self.HeadersAuth) as Response:
                return await self._Result(Response)

    async def Send(self, aPhones: list[str], aMsg: str):
        return await self._Post(
            f'{self.Url}/message',
            {
                'message': aMsg,
                'phoneNumbers': aPhones,
                'withDeliveryReport': True
            }
        )

    async def Status(self, aId: str):
        return await self._Get(f'{self.Url}/message/{aId}')

    async def Logs(self):
        return await self._Get(f'{self.Url}/logs')

    async def Health(self):
        return await self._Get(f'{self.Url}/health')
