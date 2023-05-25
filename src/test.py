import re
import barcodenumber
from Inc.Ean import TEan


def Test_01():
    #p1 = r'[\W_]'
    #p1 = r'[^\w\s]'
    #p1 = r'[^a-zA-Z0-9\s]'
    #p1 = r'''[!_"'`]\s+'''

    s1 = 'This      1   i7-1200/8GB/  / hdd 500////     _(2)" ` text [3]'
    print(s1)
    s1 = re.sub(r'[\s/]+', ' ', s1)
    s1 = re.sub(r'[^a-zA-Z0-9\s]', '', s1)
    s1 = s1.lower()
    print(s1)

def Test_02():
    Code = '48209621'
    Code = '48210721'
    Code = '5413149333529'

    #q1 = barcodenumber.check_code('ean8', Code)
    #print(q1)

    Ean = TEan(Code)
    q1 = Ean.Check()
    print(q1)


#Test_01()
Test_02()
