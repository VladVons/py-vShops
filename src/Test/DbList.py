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
    with open('export_uttc_231213.json', 'r', encoding='utf-8') as F:
        Data = json.load(F)
    DblC = TDbList().Import(Data.get('category'))
    print(len(DblC))
    DblP = TDbList().Import(Data.get('product'))
    print(len(DblP))

    with open('uttc.csv', mode='w', newline='') as F:
        csv_writer = csv.writer(F)
        csv_writer.writerow(DblP.GetFields())
        csv_writer.writerows(DblP.Data)

Test_02()
