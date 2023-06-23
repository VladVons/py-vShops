import os
import json
import asyncio
import shutil
#
from IncP.PluginEan import TPluginEan
from Inc.Misc.Crypt import CryptSimple
from Inc.Misc.FS import DirWalk


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
    Xlat = {}

    Dir = 'Data/img/product'
    for i, x in enumerate(DirWalk(f'{Dir}/0')):
        File = x[0].rsplit('/', maxsplit=1)[-1]
        Hash, Ean, Ext = File.split('_')
        EanX = CryptSimple(Ean, 71)
        DirDst = f'{Dir}/00/{EanX[-2:]}'
        os.makedirs(DirDst, exist_ok=True)
        FileDst = f'{DirDst}/{EanX}_{Ext}'

        if (i % 100 == 0):
            print(i, x[0], FileDst)
        Xlat[x[0]] = FileDst
        shutil.copyfile(x[0], FileDst)

    with open('Xlat.json', 'w') as F:
        json.dump(Xlat, F, indent=2, ensure_ascii=False)


async def Test_03():
    #PData = {'plugin': 'gepir4_gs1ua_org', 'code': '4820182065705'}
    #PData = {'plugin': 'rozetka_com_ua', 'code': '5000299618240'}
    #PData = {'plugin': 'listex_info', 'code': '4823003207513'}
    #PData = {'plugin': 'himopt_com_ua', 'code': '5903719640855'}
    #PData = {'plugin': 'via_com_ua', 'code': '5900657217927'}
    #PData = {'plugin': 'fozzyshop_ua', 'code': '4820179000788'}
    #PData = {'plugin': 'kaluna_te_ua', 'code': '4823003207513'}
    #PData = {'plugin': 'bscanner_com_ua', 'code': '-4820182745881 4850001274759'}
    #PData = {'plugin': 'artdrink_com_ua', 'code': '4049366003191'}
    PData = {'plugin': 'icecat_biz', 'code': '-33583558 -35771254 31170149'}

    PluginEan = TPluginEan('IncP/PluginEan')
    Parser = PluginEan.Load(PData['plugin'])
    await Parser.Init()
    for xCode in PData['code'].split():
        if (not xCode.startswith('-')):
            Data = await Parser.GetData(xCode)
    print(Data)


asyncio.run(Test_03())

