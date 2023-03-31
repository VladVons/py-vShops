import re
from Inc.Misc.Profiler import TStats
from Inc.Misc.Jinja import TTemplate
from Inc.DbList import TDbList

# with TStats():
#     for x in  ClassA('Hello from python'):
#         print(x)

Path1 = ['MVC/catalog/view/route/default/tpl']
File1 = 'MVC/catalog/view/route/default/tpl/common/home.j2'
DblData1 = {'head': ['title', 'age'], 'data': [['user1', 10], ['user2', 20]]}
Data1 = {
    'ctrl' : {
        'modules': {
            'category': {
                'data': DblData1
            }
        }
    }
}

# Dbl = TDbList().Import(DblData1)
# print(Dbl)

# Tpl = TTemplate(Path1)
# Res1 = Tpl.RenderFile(File1, Data1)
# print(Res1)

Text = '''
hello  
  {{ var_1   }}one
  world
  {{   var2}}
end
'''

Pattern = r'\{\{\s*(\w+)\s*\}\}'
q1 = re.findall(Pattern, Text)
print(q1)


# str = '''
# потрібно отримати списки в яких є:

# 1) base.html
# extends
# {% extends "base.html" %}

# 2) ./panel.j2
# include
# {% include './panel.j2' %}

# 3) inc_header
# {{ inc_header }}

# в кінці я маю замінити фігурні дужки і все що всередині них на мої дані.
# '''

# import re

# arr = re.findall(r'''[{]{1,2}%?\s*([a-z-_]+)\s*['"]?([^'"}]*)['"]*\s*%?[}]{1,2}''', str)
# print(arr)