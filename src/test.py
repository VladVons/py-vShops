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

#Dbl = TDbList().Import(DblData1)
#print(Dbl)

Tpl = TTemplate(Path1)
Res1 = Tpl.RenderFile(File1, Data1)
print(Res1)
