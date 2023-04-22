import asyncio
from Inc.Sql import TDbPg, TDbAuth, TDbExecPool


DbAuth = {
    'host': '10.10.1.1',
    'port': 5432,
    'database': 'shop2',
    'user': 'admin',
    'password': '098iop'
}

async def Test_1():
    Auth = TDbAuth(**DbAuth)
    Db = TDbPg(Auth)
    await Db.Connect()

    Query = '''
        select 	rp.id
        from ref_product rp
        where rp.id = 74;

        select 	rp.id
        from ref_product rp
        where rp.id = 75;
    '''
    Dbl = await TDbExecPool(Db.Pool).Exec(Query)
    print(Dbl)

    await Db.Close()

Task = Test_1()
asyncio.run(Task)
