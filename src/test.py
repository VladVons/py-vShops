import asyncio
import webbrowser
#
from IncP.PluginEan import TPluginEan


async def Test_02():
    #PData = {'plugin': 'gepir4_gs1ua_org', 'ean': '4820182065705'}
    #PData = {'plugin': 'rozetka_com_ua', 'ean': '5000299618240'}
    #PData = {'plugin': 'listex_info', 'ean': '4823003207513'}
    #PData = {'plugin': 'himopt_com_ua', 'ean': '5903719640855'}
    #PData = {'plugin': 'via_com_ua', 'ean': '5900657217927'}
    PData = {'plugin': 'fozzyshop_ua', 'ean': '4820179000788'}

    PluginEan = TPluginEan('IncP/PluginEan')
    PluginEan.Load(PData['plugin'])
    Data = await PluginEan.GetData(PData['ean'])
    print(Data)

# Url = 'https://img.fozzyshop.com.ua/229075-thickbox_default/sigareta-elektronnaya-odnorazovaya-bmor-saturn-green-apple-ice.jpg'
# webbrowser.open(Url, autoraise=True)

asyncio.run(Test_02())
