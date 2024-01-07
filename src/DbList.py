import json
import csv
#
from Inc.DbList import TDbList


def Test_01():
    Data1 = [
        ['User5', 55, True, 5.67],
        ['User2', 22, True, 2.34],
        ['User6', 66, True, 6.78],
        ['User1', 11, False, 1.23]
    ]

    Dbl1 = TDbList(
        ['User', 'Age', 'Male', 'Price'],
        Data1
    )

    Dbl1.Rec.User = 'new user'
    Dbl1.Rec.User1 = 'new user'
    Dbl1.Rec.Data[0] = '000'
    q2 = Dbl1.Rec.User2

    Data2 = [
        [1, False, 5.67],
        [2, True, 2.34],
        [3, True, 6.78],
        [4, False, 1.23]
    ]

    Dbl2 = TDbList(
        ['Order', 'Enabled', 'Rest'],
        Data2
    )

    Dbl1.MergeDbl(Dbl2, ['Order', 'Enabled'])
    print(Dbl1)

def Test_02():
    # json prettifier
    # iconv -f WINDOWS-1251 -t UTF-8 exp_oster.json | jq > exp_oster_1.json

    CP = 'cp1251'
    with open('exp_oster.json', 'r', encoding=CP) as F:
        Data = json.load(F)
        #Data = F.read()
        #Data = Data.replace(';', '|')
        #Data = json.loads(Data)

    DblC = TDbList().Import(Data.get('category'))
    print(len(DblC))
    DblP = TDbList().Import(Data.get('product'))
    print(len(DblP))
    #for Rec in DblP:
    #    print(Rec.GetAsDict())

    with open('uttc.csv', mode='w') as F:
        csv_writer = csv.writer(F, quoting=csv.QUOTE_ALL)
        csv_writer.writerow(DblP.GetFields())
        csv_writer.writerows(DblP.Data)

Test_01()
