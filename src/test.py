import re
import gspread


def Test_05():
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sht = gc.open_by_url(Url)

def Test_06():
    Dict1 = {
        'd1' : {'one': 1, 'two': 2},
        'd2': {'sunday':0, 'monday': 1},
        'd3': {'one':11}
    }
    Res = {}
    for x in Dict1.values():
        Res.update(x)
    return Res


def Test_07():
    Data = [
        [11, '12', 13],
        [21, '22', 23],
        [31, '32', 33],
        [41, '42', 43]
    ]

    #q1 = list(zip(*Data))
    #del q1[1]
    #q2 = list(zip(*q1))
    #print(q2)
    #print(*Data)

    FieldNo = 1
    if (isinstance(Data[0][FieldNo], str)):
        Res = [x[FieldNo] for x in Data]
        print('int', "'" + "', '".join(Res) + "'")
    else:
        Res = [str(x[FieldNo]) for x in Data]
        print('str', ', '.join(Res))

Test_07()
