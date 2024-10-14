Data = '''
{\n  "product": {\n    "info": {\n      "url": "https://computer7.com.ua/ua"\n    },\n    "pipe_microdata": [\n      ["product_ldjson"]\n    ],\n    "pipe_product": [\n      ["find", ["div", {"class": "cs-product__container"}]],\n      ["as_dict", {\n        "images": [\n          ["find", ["div", {"class": "cs-product__images"}]],\n          ["find_all_get_url", ["img"], {"a_get": "src"}],\n          ["list_map", [\n            ["replace", [["h100", "w100"], ["h640", "w640"]]]\n          ]]\n        ],\n        "price_old": [\n          ["find", ["div", {"class": "b-product-cost"}]],\n          ["find", ["p", {"class": "b-product-cost__old-price"}]],\n          ["text_strip"],\n          ["price"]\n        ]\n      }]\n    ],\n    "pipe_root": [\n      ["as_dict", {\n        "features": [\n          ["find", ["table", {"class": "b-product-info"}]],\n          ["table"],\n          ["keyval2dict"]\n        ],\n        "description": [\n          ["find", ["div", {"data-qaid": "product_description"}]],\n          ["text_tag", ["p"]]\n        ]\n      }]\n    ]\n  }\n}
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

