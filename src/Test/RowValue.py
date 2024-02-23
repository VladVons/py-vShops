Data = '''
-- in: aLangId, CategoryId\nselect\n    rpc.id,\n    rpc.image,\n    rpcl.title,\n    rpcl.descr,\n    rpcl.meta_key\nfrom\n    ref_product0_category rpc\nleft join\n    ref_product0_category_lang rpcl on\n    (rpcl.category_id = rpc.id) and (rpcl.lang_id = 1)\nwhere\n    rpc.enabled and\n    (rpc.id = )
'''
with open('Query.txt', 'w') as F:
    F.write(Data)

