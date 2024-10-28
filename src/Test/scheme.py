import asyncio
#from Inc.Misc.aiohttpClient import UrlGetData
from Inc.Scheme.Utils import FindLineInScheme

async def Main2():
    Path = "/product/pipe_product/find/as_dict/features/find/table1->['table1'] (unknown)"
    Path = Path.split('->', maxsplit=1)[0]

    with open('product.json', 'r', encoding='utf8') as F:
        JsonStr = F.read()
    Res = FindLineInScheme(JsonStr, Path)
    print(Res)

# async def Main1():
#     Url = 'https://a-pc.com.ua/bv-mon-tori/mon-tor-22-philips-225pl2-1680-x-1050-tft-lcd-a-b-v'

#     Data = await UrlGetData(Url)
#     print("done")

asyncio.run(Main2())
