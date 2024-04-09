Data = '''
-- fmtIns_HistUrl.sql\n\ninsert into hist_url(\n    data_size, \n    url_count, \n    status_code, \n    parsed_data, \n    url_id,\n    user_id\n)\nvalues (\n    27633, \n    53, \n    200, \n     \'{\n "name": "Gembird (4.5м) SPG5-G-15B black",\n "price": [\n  250.0,\n  "грн"\n ],\n "stock": true,\n "image": "http://oster.com.ua/image/cache/catalog/products/678811-500x500.jpg",\n "category": "Периферія, аксесуари/Мережеві фільтри",\n "sku": "678811",\n "description": null\n}\' , \n    338,\n    \n)
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

