import os
import time
import json
import asyncio
import shutil
import re
#
#from IncP.PluginEan import TPluginEan
#from Inc.Misc.Crypt import CryptSimple
#from Inc.Misc.FS import DirWalk


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
    DirSrc = 'Data/img/product/1'
    for i, x in enumerate(DirWalk(f'{DirSrc}')):
        File = x[0].rsplit('/', maxsplit=1)[-1]
        BaseName = File.split('.', maxsplit=1)[0]
        DirDst = f'{DirSrc}/x/{BaseName[:2]}'
        FileDst = f'{DirDst}/{File}'

        print(FileDst)
        #os.makedirs(DirDst, exist_ok=True)
        #shutil.copyfile(x[0], FileDst)

async def Test_04():
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

def SpeedTest(aCnt: int) -> int:
    Res = 0
    for i in range(aCnt):
        Res += i
    return Res

def mdm1():
    # data = '5x Monitor  LCD 22" ViewSonic VG2239SMH  150 zł netto/szt.'
    # pattern = r'(\d+)\s*x\s*(.*?)\s*(\d+)\s*(zł|zl|z)\s*netto'

    data = 'DELL 7390 i5-8350U 8GB 256SSD W10P COA FHD TOUCH -'
    data = 'DELL 5070 SFF I5-9500 8GB 256SSD RW W10P COA BOX'
    data = 'DELL PREC 5810 E5-1650v3 32GB 1TB RW K2200 COA'
    #data = 'DELL T7910 2xE5-2630v4 64GB 2x1TB DVD COA M4000'
    #pattern = r'(.*?)\s*((\d+x)*[ie]\d+-\w+)\s*(\d+[GT]B)\s*((\d+x)*\d+([GT]B))'
    #pattern = r'(.*?)\s*(\d*x?[ie]\d+-\w+)\s*(\d+GB)\s*(\d*x?\d+[GT]B)'
    pattern = r'(.*?)\s*(\d*x?[ie]\d+-\w+)\s*(\d+GB)\s*(\d+\w+)'
    #pattern = r'\d*x?E5-2630v4'

    matches = re.findall(pattern, data, re.IGNORECASE)
    print(matches)
    return

    with open('mdm.txt', 'r', encoding='utf8') as F:
        Lines = F.readlines()

    PtrnMonit = r'(\d+)\s*x(.*?)(\d*)\"\s*(.*?)\s*(\d+)\s*(zł|zl|z)\s*netto'
    PtrnBody = r'(\d+)\s*x\s*(.*?)\s*(\d+)\s*(zł|zl|z)\s*'
    for Line in Lines:
        # if ('Monitor' in Line):
        #     Matches = re.findall(PtrnMonit, Line)
        #     if (Matches):
        #         pass
        #         print(Matches)
        #     else:
        #         print(Line)

        Matches = re.findall(PtrnBody, Line)
        if (Matches):
            pass
            print(Matches)
        else:
            print(Line)

def mdm():
    with open('mdm.txt', 'r', encoding='utf8') as F:
        Lines = F.readlines()

    # data = '5x Monitor  LCD 22" ViewSonic VG2239SMH  150 zł netto/szt.'
    # data = '5x DELL 7390 i5-8350U 8GB 256SSD W10P COA FHD TOUCH -  150 zł netto/szt.''
    # data = '5x DELL 5070 SFF I5-9500 8GB 256SSD RW W10P COA BOX 150 zł netto/szt.''
    # data = '5x DELL PREC 5810 E5-1650v3 32GB 1TB RW K2200 COA 150 zł netto/szt.''

    ReBody = re.compile(r'(\d+)\s*x\s*(.*?)[\s-]*(\d+)\s*z', re.IGNORECASE)
    ReMonit = re.compile(r'(\d*)\"\s*(.*?)$', re.IGNORECASE)
    ReMonitDel = re.compile(r'Monitor LCD \d+"\s', re.IGNORECASE)
    ReComputer = re.compile(r'(.*?)\s*(\d*x?[ie]\d+-\w+)\s*(\d+GB)\s*(\d+\w+)', re.IGNORECASE)
    for Line in Lines:
        MatchBody = ReBody.findall(Line)
        if (MatchBody):
            Qty, Body, Price = MatchBody[0]
            if ('Monitor' in Line):
                Category = 'Монітор'
                Matches = ReMonit.findall(Body)
                if (Matches):
                    Model = Matches[0][1]
                    Body = ReMonitDel.sub('', Body)
            elif any(s in Body for s in [' HD', ' FHD', ' QHD']):
                Category = 'Ноутбук'
                Matches = ReComputer.findall(Body)
                if (Matches):
                    Model = f'{Matches[0][0]} {Matches[0][1]}'
            else:
                Category = 'Компютер'
                Matches = ReComputer.findall(Body)
                if (Matches):
                    Model = f'{Matches[0][0]} {Matches[0][1]}'

            if (Matches):
                print(f'{Category}, {Model}, {Qty}, {Price}, {Body}')
            else:
                print('Err', Category, Body)


#Time = time.time()
#SpeedTest(100000000)
#print('done', time.time() - Time)

mdm()
#asyncio.run(Test_03())
