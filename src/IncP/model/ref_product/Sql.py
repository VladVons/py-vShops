# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re


def GetProducts(aLangId: int, aText: str) -> str:
    Title = [f"('%{x}%')" for x in re.split(r'\s+', aText)]
    Title = ', '.join(Title)

    return f'''
    select
        rp.id,
        rp.idt,
        rp.tenant_id,
        rpl.title
    from
        ref_product rp
    left join
        ref_product_lang rpl on
        (rp.id = rpl.product_id)
    where
        (rpl.lang_id = {aLangId}) and
        (rpl.title ilike all (values {Title}))
    '''

def AddHistProductSearch(aLangId: int, aSessionId: int, aText: str):
    return f'''
        insert into hist_product_search (lang_id, session_id, context)
        values ({aLangId}, {aSessionId}, '{aText}')
    '''
