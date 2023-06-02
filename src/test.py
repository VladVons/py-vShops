import asyncio
import webbrowser
#
from IncP.PluginEan import TPluginEan

async def Test_01():
    Data = '''
        Rozetka,  Watsons,  MAUDAU,  EVA,  Епіцентр,  Сільпо,  Метро,  АТБ,  MAKEUP,  PAMPIK,  EXIST.UA,  F.UA,  WINETIME,  AURA,  Masmart,
        e-Coffee.com.ua,  KidButik.ua,  Подорожник,  MIKSON,  АГУСИК,  iHerb,  Lantale,  Raptom,  Канцелярка,  Кофейня,  Престиж Плюс,
        Rumiana,  IpopoKids,  SOLO,  SportShop,  МОБИЛЛАК,  VINTAGE,  ISEI,  Аптека24,  ArtDrink,  PAPAY,  Кідіс,  Антошка,  BROCARD,
        Полиця,  Ли́тали,  PROSTOR,  Наша Стройка,  Книгарня "Є",  Мегакнига,  Detmir,  Країна казок,  Фаунамаркет,  zootovary.net.ua, 
        Tabletki.ua,  Рово,  Хім Опт,  eBay,  Inter Cars, Rozetka,  Watsons,  MAUDAU,  MAKEUP,  PAMPIK,  EXIST.UA,  F.UA,  WINETIME,  AURA,  
        Masmart,  e-Coffee.com.ua,  KidButik.ua, Подорожник,  MIKSON,  АГУСИК,  iHerb,  Lantale,  Raptom,  Канцелярка,  Кофейня,  Престиж Плюс,  Rumiana,  IpopoKids,  SOLO,  
        SportShop,  МОБИЛЛАК,  VINTAGE,  Аптека24,  ArtDrink,  PAPAY,  Кідіс,  Антошка,  BROCARD,  Полиця,  Ли́тали,  PROSTOR,  Наша Стройка,  
        Книгарня "Є",  Мегакнига,  Detmir,  Країна казок,  Фаунамаркет,  zootovary.net.ua,  Рово,  Хім Опт,  eBay,  Inter Cars
    '''

    Data = set([x.strip().lower() for x in Data.split(',')])
    print(len(Data))
    print(sorted(Data))



async def Test_02():
    #PData = {'plugin': 'gepir4_gs1ua_org', 'ean': '4820182065705'}
    #PData = {'plugin': 'rozetka_com_ua', 'ean': '5000299618240'}
    #PData = {'plugin': 'listex_info', 'ean': '4823003207513'}
    #PData = {'plugin': 'himopt_com_ua', 'ean': '5903719640855'}
    #PData = {'plugin': 'via_com_ua', 'ean': '5900657217927'}
    #PData = {'plugin': 'fozzyshop_ua', 'ean': '4820179000788'}
    PData = {'plugin': 'kaluna_te_ua', 'ean': '4823003207513'}

    #PData = {'plugin': 'bscanner_com_ua', 'ean': '4820182745881'}
    #PData = {'plugin': 'bscanner_com_ua', 'ean': '4850001274759'}

    #PData = {'plugin': 'artdrink_com_ua', 'ean': '4049366003191'}

    PluginEan = TPluginEan('IncP/PluginEan')
    Parser = PluginEan.Load(PData['plugin'])
    await Parser.Init()
    Data = await Parser.GetData(PData['ean'])
    print(Data)

asyncio.run(Test_02())

