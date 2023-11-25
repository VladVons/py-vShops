import asyncio
from jinja2 import Template
#
from Inc.DbList import TDbList
from Task.SrvModel.Api import ApiModel


Data1 = [
    'system',
    {
        'method': 'Get_ConfTenant',
        'param': {'aTenantId': 0}
    }
]

Data2 = [
    'system',
    {
        'method': 'Get_SeoToDict_LangPath',
        'param': {
            'aLangId': 1,
            'aPath': ['mp3-players', 'test-15', 'ua', 'catalog']
        }
    }
]

Data3 = [
    'ref_product0/category',
    {
        'method': 'Get_CategoriesSubCount_ParentLang',
        'param': {
            'aLang': 'ua',
            'aParentIdRoot': 0
        }
    }
]

async def Test_01():
    # def CategoryTreeList_():
    #     nonlocal Dbl, BTree

    #     ParentId = Dbl.Rec.parent_id
    #     while (not Dbl.EOF()) and (Dbl.Rec.parent_id == ParentId):
    #         print(Dbl.Rec)
    #         RecNo = BTree.Search(Dbl.Rec.id)
    #         if (RecNo >= 0):
    #             CurRec = Dbl.RecNo
    #             Dbl.RecGo(RecNo)
    #             CategoryTreeList()
    #             Dbl.RecGo(CurRec)
    #         Dbl.Skip()

    # def CategoryTreeList_():
    #     nonlocal Dbl, BTree

    #     ParentId = Dbl.Rec.parent_id
    #     while (not Dbl.EOF()) and (Dbl.Rec.parent_id == ParentId):
    #         print(Dbl.Rec)
    #         RecNo = BTree.Search(Dbl.Rec.id)
    #         if (RecNo >= 0):
    #             CurRec = Dbl.RecNo
    #             Dbl.RecGo(RecNo)
    #             CategoryTreeList()
    #             Dbl.RecGo(CurRec)
    #         Dbl.Skip()


    def CategoryTreeList(aKey):
        nonlocal Categories

        for x in Categories[aKey]:
            print(x)

            Id = x['id']
            if (Id in Categories):
                CategoryTreeList(Id)


    await ApiModel.DbConnect()
    Data = await ApiModel.Exec(*Data3)
    DblData = Data.get('data')
    if (DblData):
        Dbl = TDbList().Import(DblData)
        print(Dbl)

        Categories = {}
        for Rec in Dbl:
            ParentId = Dbl.Rec.parent_id
            if (ParentId not in Categories):
                Categories[ParentId] = []
            Categories[ParentId].append(Rec.GetAsDict())
        #CategoryTreeList(0)
        template = Template("""
            <ul class="navbar-nav" title="categories">
                <li class="nav-item dropdown" id="viMainNavbar">
                    <a class="nav-link dropdown-toggle" data-bs-toggle="dropdown"  href="#"><i class="fa fa-bars" style="font-size: 2.0em;"></i></a>
                    <ul class="dropdown-menu">

                    {%- for x in Categories[id] recursive %}
                        {%- if x.id in Categories %}
                            <li class="nav-item dropdown">
                                <a class="dropdown-item dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">{{ x.title }}</a>
                                <ul class="dropdown-menu">
                                    {{ loop(Categories[x.id])}}
                                </ul>
                            </li>
                        {%- else %}
                            <li><a class="dropdown-item" href="#">{{ x.title }}</a></li>
                        {%- endif %}
                    {%- endfor %}

                    </ul>
                </li>
            </ul>
        """)

        print(template.render(Categories=Categories, id=0))

    await ApiModel.DbClose()


asyncio.run(Test_01())
