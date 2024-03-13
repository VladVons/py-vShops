Data = '''
-- fmtGet_News.sql\n-- in: aNewsId, aLangId\n\nselect\n    coalesce(rn.public_date, rn.create_date)::date as date,\n    rnl.title,\n    rnl.descr,\n    rnl.meta_key \nfrom\n    ref_news rn \njoin\n    ref_news_lang rnl on\n    (rnl.news_id = rn.id) and (rnl.lang_id = 1)\nwhere\n    (rn.enabled) and\n    (rn.id = 1)\n    ((rn.public_date < now()) or (rn.public_date is null)) and\n    (tenant_id = 0)
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

