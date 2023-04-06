# Created: 2023.03.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# https://www.youtube.com/watch?v=bu5wXjz2KvU
# https://console.developers.google.com


import gspread


def Test_05():
    #Auth = '~/.config/gspread/service_account.json'
    gc = gspread.service_account()

    Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
    sh = gc.open_by_url(Url)
    wsl = sh.worksheets()
    ws = sh.worksheet('MONITORS')
    print(ws.row_count, ws.col_count)
    Values = ws.get_all_values()
    

    pass

Test_05()
