# Created: 2024.02.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://developers.novaposhta.ua/documentation
# Token = 'a2159266677aa6452fa8f6b01c7fb71e'
# NovaPoshta = TNovaPoshta(Token)
# Res = await NovaPoshta.SearchtAddress('терноп')
# Ref = Res['data'][0]['Addresses'][0]['Ref']
# Res = await NovaPoshta.SearchtStreet('Живова', Ref)


import asyncio
import aiohttp


class TNovaPoshta():
    def __init__(self, aToken: str):
        self.Token = aToken
        self.Url = 'https://api.novaposhta.ua/v2.0/json/'
        self.Limit = 10

    @staticmethod
    async def Request(aUrl: str, aData: dict):
        async with aiohttp.ClientSession() as Session:
            async with Session.post(aUrl, json=aData) as Response:
                return await Response.json()

    async def SearchtAddress(self, aName: str) -> dict:
        Data = {
            "apiKey": self.Token,
            "modelName": "Address",
            "calledMethod": "searchSettlements",
            "methodProperties": {
                "CityName" : aName,
                "Limit" : self.Limit
            }
        }
        return await self.Request(self.Url, Data)

    async def SearchtStreet(self, aName: str, aRef: str) -> dict:
        Data = {
            "apiKey": self.Token,
            "modelName": "Address",
            "calledMethod": "searchSettlementStreets",
            "methodProperties": {
                "StreetName" : aName,
                "SettlementRef" : aRef,
                "Limit" : self.Limit
            }
        }
        return await self.Request(self.Url, Data)

    async def SettlementAreas(self) -> dict:
        Data = {
            "apiKey": self.Token,
            "modelName": "Address",
            "calledMethod": "getSettlementAreas"
        }
        return await self.Request(self.Url, Data)

    async def SettlementRegions(self, aRef: str) -> dict:
        Data = {
            "apiKey": self.Token,
            "modelName": "Address",
            "calledMethod": "getSettlementCountryRegion",
            "methodProperties": {
                "AreaRef" : aRef
            }
        }
        return await self.Request(self.Url, Data)

    async def Cities(self, aRef: str) -> dict:
        Data = {
            "apiKey": self.Token,
            "modelName": "Address",
            "calledMethod": "getCities",
            "methodProperties": {
                "Ref" : aRef
            }
        }
        return await self.Request(self.Url, Data)

async def GetRegions(aNovaPoshta):
    Areas = await aNovaPoshta.SettlementAreas()
    for xArea in Areas['data']:
        print(' ' * 1, xArea['Description'])
        Regions = await aNovaPoshta.SettlementRegions(xArea['Ref'])
        for xRegions in Regions['data']:
            print(' ' * 2, xRegions['Description'])
