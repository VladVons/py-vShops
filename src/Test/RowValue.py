Data = '''
\n                with src_data (lang_id, product_id, attr_alias, val) as (\n                    values \n                ),\n                mapper as (\n                    select\n                        src_data.lang_id,\n                        src_data.product_id,\n                        ra.id,\n                        src_data.val\n                    from\n                        src_data\n                    join\n                        ref_attr ra\n                        on (src_data.attr_alias = ra.alias)\n                )\n                merge into ref_product_attr as dst\n                using mapper as src\n                on (dst.product_id = src.product_id) and (dst.lang_id = src.lang_id) and (dst.attr_id = src.id)\n                when matched then\n                    update set val = src.val\n                when not matched then\n                    insert (product_id, lang_id, attr_id, val)\n                    values (src.product_id, src.lang_id, src.id, src.val)\n            
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

