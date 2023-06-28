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


#asyncio.run(Test_03())
q1 = {
    "size": [
        ["4820052669897", ""], 
        ["Висота, см", "7.9"], 
        ["Глибина, см", "5.4"], 
        ["Ширина, см", "5.6"], 
        ["Вага брутто, кг", "0.218"], 
        ["4820052669880", "Коробка (24 шт)"], 
        ["Висота, см", "8.6"], 
        ["Глибина, см", "42.8"], 
        ["Ширина, см", "17.8"], 
        ["Вага брутто, кг", "5.388"], 
        ["Ознака викладки шоубокс", "НІ"]
    ], 
    "name": [
        ["Назва (рос.)", "Коктейль молочный 2.5% Сливочно-ванильный Paw Patrol Danone т/п 212г"], 
        ["Назва (укр.)", "Коктейль молочний 2.5% Вершково-ванільний Paw Patrol Danone т/п 212г"], 
        ["Коротка назва (рос.)", "Коктейль молочный Слив-ванил Danone 212г"], 
        ["Коротка назва (укр.)", "Коктейль молочний Верш-ваніл Danone 212г"], 
        ["Альтернативне найменування (рос)", "Коктейль молочный Danone Paw Patrol со Сливочно-ванильный 2.5% 212г"], 
        ["Альтернативне найменування (укр)", "Коктейль молочний Danone Paw Patrol Вершково-ванільний 2.5% 212г"]
    ], 
    "misc": [
        ["Смак", "ВЕРШКОВО-ВАНІЛЬНИЙ"], 
        ["Вид продукції", "КОКТЕЙЛЬ МОЛОЧНЫЙ"], 
        ["Ваговий товар", "НІ"], ["Кількість, шт.", "1"], 
        ["Планограма викладення товару", "ТАК"], 
        ["Рекомендовані способи приготування/використання", "Перед вживанням збовтати"]
    ], 
    "nutrition": [
        ["Жири, г/100г", "2.5"], 
        ["Білки, г/100г", "3.2"], 
        ["Вуглеводи, г/100г", "9.9"], 
        ["Жирність, %", "2.5"], 
        ["Калорійність, ккал/100г", "75"], 
        ["кДж/100г", "314"], 
        ["Цукор, г/100г", "9.9"]
    ], 
    "main": [
        ["Метод обробки", "СТЕРИЛІЗАЦІЯ"], 
        ["ГМО", "НІ"], 
        ["Органічний продукт", "НІ"], 
        ["Підходить вегетаріанцям", "ТАК"], 
        ["Підходить веганам", "НІ"]
    ], 
    "ingredients": [
        ["Склад (рос.)", "Молоко нормализованное 95%, сахар, ароматизатор натуральный \"сливочно-ванильный\", стабилизатор каррагинан, краситель бета-каротин"], 
        ["Склад (укр.)", "Молоко нормалізоване 95%, цукор, ароматизатор натуральний \"вершково-ванільний\", стабілізатор карагенан, барвник бета-каротин"], 
        ["Склад (оригінал)", "Normalized milk 95%, sugar, flavoring natural \"creamy-vanilla\", carrageenan stabilizer, beta-carotene dye"]
    ], 
    "retention": [
        ["Термін придатності, дн.", "150"], 
        ["Мін. температура", "+1"], 
        ["Макс. температура", "+20"], 
        ["Температура зберігання, ºC", "+1..+20"], 
        ["Навколишнє середовище", "СУХОЕ МЕСТО/БЕЗ ПОПАДАНИЯ ПРЯМЫХ СОЛНЕЧНЫХ ЛУЧЕЙ"], 
        ["Термін придатності, днів", "150"]
    ]
}

q2 = {
    "Дисплей": [
        "Діагональ дисплею: 50,8 см (20\")", 
        "Роздільна здатність дисплея: 1680 x 1050 пікселів", 
        "Сенсорний екран: Ні", 
        "Яскравість дисплея (типова): 300 кд/м²", 
        "Час відклику: 5 мс", 
        "Контрасність (типічна): 1000:1", 
        "Кут огляду по горизонталі: 170°", 
        "Кут огляду по вертикалі: 170°", 
        "Розмір точки: 0.258", 
        "Горизонтальна частота сканування: 30 - 82 кГц", 
        "Вертикальна частота сканування: 55 - 75 Гц", 
        "Видима область екрану по горизонталі: 43,3 см", 
        "Видима область екрану по вертикалі: 27,1 см"
    ], 
    "Дизайн": [
        "Колір продукту: Сірий", 
        "Сертифікація: TCO’03"
    ], 
    "Порти та інтерфейси": [
        "Кількість портів VGA (D-Sub): 1", 
        "Кількість портів DVI-D: 1"
    ], 
    "Ергономіка": [
        "Слот кабельного блокування: Так", 
        "Тип слоту кабельного блокування: Kensington", 
        "Настроювання висоти: 11 см", 
        "Діапазон кутів обертання: 45 - 45°", 
        "Кут нахилу: -5 - 30°"
    ],
    "Енергоживлення": [
        "Споживча потужність (типічна): 45 Вт", 
        "Споживча потужність (вимк.): 1 Вт", 
        "Споживча потужність (режим економії енергії): 1 Вт"
    ], 
    "Вага та розміри": [
        "Ширина з підставкою: 474 мм", 
        "Глибина з підставкою: 212 мм", 
        "Висота з підставкою: 399 мм", 
        "Вага (з підставкою): 7 кг", 
        "Ширина (без підставки): 47,4 см", 
        "Глибина (без підставки): 5,8 см", 
        "Висота (без підставки): 32 см", 
        "Вага (без підставки): 4,2 кг"
    ], 
    "Інші характеристики": [
        "Вимоги до енергоживлення: 100 - 240 VAC, 50 - 60 Hz"
    ]
}

q3 = {
    "main": [
        ["Бренд", "Rothmans"], 
        ["Фасовка", "пачка"], 
        ["Країна", "Україна"], 
        ["Вид продукції", "Сигарети"], 
        ["Бренд", "Rothmans"], 
        ["Аромат", "Класичний"], 
        ["Вміст нікотину, мг", "0,6"], 
        ["Вміст смол, мг", "8"], 
        ["К-ть в упаковці, шт.", "20"], 
        ["Розмір", "King Size"]
    ]
}

q4 = {
    "main": [
        "Перець пепероні 50%", 
        "вода питна", 
        "цукор білий", 
        "сіль кухонна харчова", 
        "консервант оцтова кислота", 
        "прянощі: зерна гірчиці, перець чорний горошок, лавровий лист, часник, кріп, цибуля."
    ]
}

q5 = [
    "Перець пепероні 50%", 
    "вода питна", 
    "цукор білий", 
    "сіль кухонна харчова", 
    "консервант оцтова кислота", 
    "прянощі: зерна гірчиці, перець чорний горошок, лавровий лист, часник, кріп, цибуля."
]


def FeaturesAdjast(aObj: object, aDepth: int):
    if (isinstance(aObj, dict)):
        for xKey, xVal in aObj.items():
            print()
            print('group', xKey)
            FeaturesAdjast(xVal, aDepth + 1)
    elif (isinstance(aObj, list)):
        for xVal in aObj:
            if (len(xVal) == 2):
                xVal = ': '.join(xVal)
            print(xVal)
        
print()
FeaturesAdjast(q5, 0)
