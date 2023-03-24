from Inc.DbList import TDbList, TDbRec
from Inc.Misc.Profiler import Profiler


def Test01(aA1, aB1):
    print(aA1, aB1)

    Data = [
            ['User', 'Age', 'Male', 'Price'],
            [
                ['User5', 55, True, 5.67],
                ['User2', 22, True, 2.34],
                ['User6', 66, True, 6.78]
            ]
    ]


    Dbl1 = TDbList(*Data)
    D0 = [10, 20]
    D1 = [11, 21]

    Dbl1.AddFields(['q1', 'q2'], [D0, D1])
    for Idx, Rec in enumerate(Dbl1):
        print(Idx, Rec.Data)

    return 'done'

Res = Profiler(Test01, [1, 2])
print(Res)
