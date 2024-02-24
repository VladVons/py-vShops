import json
import csv
#
from Inc.DbList import TDbList


def Test_01():
    Data1 = [
        ['User5', 55, True, 5.67],
        ['User2', 22, True, 2.34],
        ['User6', 66, True, 6.78],
        ['User1', 11, False, 1.23],
        ['User3', 33, True, 3.45],
        ['User4', 44, True, 4.56],
        ['User5', 55, True, 5.55]
    ]

    Dbl1 = TDbList(
        ['User', 'Age', 'Male', 'Price'],
        Data1
    )
    Str1 = Dbl1.GetRepr()
    with open('dbl.txt', 'w', encoding='utf8') as F:
        F.write(Str1)
    return

    #print(Dbl1)
    Pairs = Dbl1.ExportPairs('Age', ['User', 'Price'])
    print(Pairs)

    Dict = Dbl1.ExportDict(['User', 'Price'])
    print(Dict)

    for Idx, Rec in enumerate(Dbl1):
        #print(Idx, Rec.GetField('User'))
        print(Idx, Rec.GetAsDictFields(['User', 'Age']))
        #print(Idx, Rec.GetAsListFields(['User', 'Age']))

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
