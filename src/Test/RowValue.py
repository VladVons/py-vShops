Data = '''
-- fmtUpd_ProductsAttr.sql\n-- in: aValues\n\nupdate\n  ref_product rp\nset\n  attr = src.attr,\n  title_crc = hashtext(src.title)\nfrom (\n  values (97746, \'Dell PowerEdge R740xd 28x 2,5 2x Gold 6154 256GB H740P 4x 1,6TB SSD 12x2TB\', \'{"category": "server", "brand": "dell", "model": "poweredge r740xd", "storage": {"size": 256, "unit": "gb", "type": "hdd"}}\'::jsonb), (35696, \'Корпус Delux MK330 Black 400W 12Fan\', \'{"case": "tower"}\'::jsonb) \n  as src(url_id, title, attr)\nwhere \n  rp.url_id = src.url_id
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

