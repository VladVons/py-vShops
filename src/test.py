import re


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

Test_01()
