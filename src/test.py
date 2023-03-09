import gspread


def Test_05():
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sht = gc.open_by_url(Url)

Test_05()



Dict1 = {
    'd1' : {'one': 1, 'two': 2},
    'd2': {'sunday':0, 'monday': 1},
    'd3': {'one':11}
}

Res = {}
for x in Dict1.values():
    Res.update(x)
return Res

