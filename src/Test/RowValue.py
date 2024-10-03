Data = '''
-- fmtSet_Site.sql\n\n  merge into ref_site as dst\n  using (\n    values (('https://it-outlet.com.ua', 1))\n  ) as src (url, country_id)\n  on (dst.url = src.url)\n  when matched then\n    do nothing\n  when not matched then\n    insert (url, country_id)\n    values (src.url, src.country_id)\n  ;\n\n  select id, url\n  from ref_site\n  where url in ('https://it-outlet.com.ua')\n  ;\n
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

