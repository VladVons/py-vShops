import re
import hashlib


def Test_01():
    p1 = r'[^\w]'
    q1 = 'This 1     _(2))" ` text [3]'
    #q2 = re.sub(p1, '', q1).lower()
    #print(q2)
    h1 = hash(''.join(sorted(list('1231'))))
    h2 = hash(''.join(sorted(list('132'))))
    print(h1)
    print(h2)
    #h1 = hex(hash(frozenset('13421')) & 0xFFFFFFFFFFFFFFFF)[2:]
    #h2 = hex(hash(frozenset('3421')) & 0xFFFFFFFFFFFFFFFF)[2:]
    #print(h1)
    #print(h2)

Test_01()
