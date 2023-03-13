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
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Mozilla/5.0 (Linux; Android 10; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Wget/1.21.2',
        'curl/7.81.0'
    ]


    def RegSession(aUserAgent: str):
        # Data  = [
        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        # 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0',
        # 'Mozilla/5.0 (Linux; Android 10; M2004J19C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36',
        # 'Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
        # 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0',
        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0',
        # 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        # 'Wget/1.21.2',
        # 'curl/7.81.0'
        # ]

        #UserAgent = self.Request.headers.get('User-Agent')

        OS = ''
        Browser = ''
        Pattern = r"\((.*?)\).*(chrome|firefox|safari|opr|gecko$)/*(.*)"
        try:
            UArr = re.findall(Pattern, aUserAgent, re.IGNORECASE)
            if (UArr):
                OS = UArr[0][0].split(';')[1].strip()
                Browser = f'{UArr[0][1]}-{UArr[0][2]}'
            else:
                Browser = aUserAgent[:16]
        except Exception:
            pass
        print(OS.lower(), Browser.lower())

    #Pattern = r"\((.*?)\)(\s|$)|(.*?)\/(.*?)(\s|$)"
    #Pattern = r"\((.*?)\).*((Chrome|Firefox|Safari|OPR).*)\s*(Mobile)*\s*"
    #Pattern = r"\((.*?)\).*(Chrome|Firefox|Safari|OPR)/(.*)\s*"
    #Pattern = r"\((.*?)\).*(Wget|Chrome|Firefox|Safari|OPR|Gecko$)/*(.*)"
    for i, x in enumerate(Data):
        RegSession(x)


Test_07()