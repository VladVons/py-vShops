import asyncio
import aiohttp
#
from Inc.Misc.NovaPoshta import TNovaPoshta, GetRegions


async def Main():
    Token = 'a2159266677aa6452fa8f6b01c7fb71e'
    NovaPoshta = TNovaPoshta(Token)
    await GetRegions(NovaPoshta)


    Res = await NovaPoshta.SearchtAddress('терноп')
    Ref = Res['data'][0]['Addresses'][0]['Ref']
    Res = await NovaPoshta.SearchtStreet('Живова', Ref)
    print('done')

asyncio.run(Main())
