from Inc.DbList import TDbList


def Test_01():
    Data = [
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
        Data
    )

    #print(Dbl1)
    Pairs = Dbl1.ExportPairs('Age', ['User', 'Price'])
    print(Pairs)

Test_01()