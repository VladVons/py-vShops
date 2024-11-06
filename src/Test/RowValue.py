Data = '''
{\n  "category": {\n  },\n  "pipe": [\n    ["as_dict", {\n      "products": [\n        ["find", ["ul", {"data-catalog-view-block": "products"}]],\n        ["find_all", ["li", {"itemprop": "itemListElement"}]],\n        ["list_map", [\n          ["as_dict", {\n            "href": [\n              ["find", ["a", {"class": "catalogCard-image"}]],\n              ["get", ["href"]],\n              ["url_pad"]\n            ],\n            "name": [\n              ["find", ["div", {"class": "catalogCard-title"}]],\n              ["find", ["a"]],\n              ["get", ["title"]]\n            ],\n            "stock": [\n              ["find_not", ["a", {"class": "__grayscale"}]]\n            ],\n            "price": [\n              ["find", ["div", {"class": "catalogCard-price"}]],\n              ["text_strip"],\n              ["price"]\n            ]\n          }]\n        ]]\n      ],\n      "pager": [\n        ["find", ["nav", {"class": "pager"}]],\n        ["find_all_get_url", ["a"], {"a_get": "href"}]\n      ]\n    }]\n  ]\n}\n}
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

