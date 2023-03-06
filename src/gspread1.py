import gspread
gc = gspread.service_account()

Url = 'https://docs.google.com/spreadsheets/d/1EIwjTitfj1_oyWS7ralnUCtq8ZH0g3DWBKq3gP4qrvo/edit#gid=782031503'
sht = gc.open_by_url(Url)
