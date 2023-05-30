import asyncio
import requests
from IncP.PluginEan import TPluginEan


def WriteFile(aName: str, aData):
    with open(aName, 'wb') as F:
        F.write(aData)


def Test_01():
    url = "https://barcodes1.p.rapidapi.com/"
    querystring = {"query": "5099206092723"}
    headers = {
        "X-RapidAPI-Key": "9d4fed06e8msh1bba3309889ce47p1cf00bjsn6d36087ed9d5",
        "X-RapidAPI-Host": "barcodes1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())


async def Test_02():
    #PData = {'plugin': 'gepir4_gs1ua_org', 'ean': '4820182065705'}
    #PData = {'plugin': 'rozetka_com_ua', 'ean': '5000299618240'}
    #PData = {'plugin': 'listex_info', 'ean': '4823003207513'}
    #PData = {'plugin': 'himopt_com_ua', 'ean': '5903719640855'}
    PData = {'plugin': 'via_com_ua', 'ean': '5900657217927'}

    PluginEan = TPluginEan('IncP/PluginEan')
    PluginEan.Load(PData['plugin'])
    Data = await PluginEan.GetData(PData['ean'])
    print(Data)

asyncio.run(Test_02())
