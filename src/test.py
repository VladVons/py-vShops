import json
import random
import asyncio
import names

from Inc.DbList import TDbList, TDbRec
from Inc.Sql.DbPg import TDbPg
from Inc.Sql.ADb import TDbAuth, TDbExecPool


async def Test_01():
    Rec = TDbRec()
    Data = [
        ['User5', 55, True, 5.67],
        ['User2', 22, True, 2.34],
        ['User6', 66, True, 6.78],
        ['User1', 11, False, 1.23]
    ]

    Fields = ['User', 'Age', 'Male', 'Price']

    Dbl1 = TDbList(
        Fields,
        Data
    )

    #Rec.Data = Data[0]
    #Rec.Fields = Fields
    #print(Rec)

    for Idx, Rec in enumerate(Dbl1): #type: TDbRec
        print(Idx, Rec.User)



Task = Test_01()
asyncio.run(Task)
