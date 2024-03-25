import asyncio
from Inc.Misc.NovaPoshta import TNovaPoshta, GetRegions


async def Main():
    Token = 'a2159266677aa6452fa8f6b01c7fb71e'
    NovaPoshta = TNovaPoshta(Token)
    #await GetRegions(NovaPoshta)

    ResAddr = await NovaPoshta.SearchtAddress('тернопі')
    StreetRef = ResAddr['data'][0]['Addresses'][0]['Ref']
    Res1 = await NovaPoshta.SearchtStreet('Живо', StreetRef)

    City = ResAddr['data'][0]['Addresses'][0]['MainDescription']
    Res2 = await NovaPoshta.Warehouses('медова', City)
    print('done')

asyncio.run(Main())
