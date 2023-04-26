import asyncio
#
from Inc.DbList import TDbList
from Task.SrvModel.Api import ApiModel


Data1 = [
    'system',
    {
        'method': 'Get_ConfTenant',
        'param': {'aTenantId': 0}
    }
]

Data2 = [
    'system',
    {
        'method': 'Get_SeoToDict_LangPath',
        'param': {
            'aLangId': 1,
            'aPath': ['mp3-players', 'test-15', 'ua', 'catalog']
        }
    }
]

async def Test_01():
    await ApiModel.DbConnect()
    Data = await ApiModel.Exec(*Data2)
    DblData = Data.get('data')
    if (DblData):
        Dbl = TDbList().Import(DblData)
        print(Dbl)
        Path = '&'.join(Dbl.ExportStr(['attr', 'val'], '{}={}'))
        print(Path)

    await ApiModel.DbClose()


asyncio.run(Test_01())
