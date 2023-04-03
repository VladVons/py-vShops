# https://habr.com/ru/post/254425
#
# 1M rows, 0.6 sec
#
# select *
# from test_json
# where
# 	(conf -> 'age' = '34') and
# 	(conf -> 'name' = '"Rick"') and
# 	(conf -> 'weight' > '50.5')
# order by id;


import sys
import json
import random
import asyncio
import names

sys.path.append('..')
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.ADb import TDbAuth, TDbExecPool


class TDbPump():
    def __init__(self):
        DbAuth = {
            'host': '192.168.2.106',
            'port': 5432,
            'database': 'shop2',
            'user': 'admin',
            'password': '098iop'
        }
        self.Db = TDbPg(TDbAuth(**DbAuth))
        self.Table = 'test_json'

    async def CreateTable(self):
        Query = f'''
            create table if not exists {self.Table} (
                id      serial primary key,
                name    varchar(32) not null,
                conf    jsonb
            );
        '''
        await TDbExecPool(self.Db.Pool).Exec(Query)

    def GenRow(self, aCount: int) -> iter:
        for _i in range(aCount):
            Name = names.get_first_name(gender='male')
            Age = random.randint(15, 70)
            Weight = round(40 + random.random() * 40, 2)
            yield {'name': Name, 'age': Age, 'weight': Weight}

    async def InsertBlock(self, aBlockSize: int):
        Values = []
        for Row in self.GenRow(aBlockSize):
            Data = json.dumps({'name': Row['name'], 'age': Row['age'], 'weight': Row['weight']})
            Values.append(f"('{Row['name']}', '{Data}')")

        Query = f'''
            insert into {self.Table} (name, conf)
            values {', '.join(Values)}
            ;
        '''
        #print(Query)
        await TDbExecPool(self.Db.Pool).Exec(Query)

    async def Exec(self, aBlockSize: int, aBlocks: int):
        await self.Db.Connect()
        for i in range(aBlocks):
            print(i+1, aBlocks)
            await self.InsertBlock(aBlockSize)
        await self.Db.Close()


async def Test_01():
    Pump = TDbPump()
    await Pump.Exec(10_000, 6)


Task = Test_01()
asyncio.run(Task)
