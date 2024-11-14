Data = '''
{\n            "@context": "http://schema.org",\n            "@type": "BreadcrumbList",\n            "itemListElement": [\n            {\n            "@type": "ListItem",\n            "position": 1,\n            "item": "https://www.vedion.pl/laptopy-poleasingowe",\n            "name": "Laptopy poleasingowe"\n            }\n        ,\n            {\n            "@type": "ListItem",\n            "position": 2,\n            "item": "https://www.vedion.pl/pl/menu/laptopy-poleasingowe/przekatna-ekranu-laptopa-1029.html",\n            "name": "Przekątna ekranu laptopa"\n            }\n        ,\n            {\n            "@type": "ListItem",\n            "position": 3,\n            "item": "https://www.vedion.pl/pl/menu/laptopy-poleasingowe/przekatna-ekranu-laptopa/laptopy-14-1032.html",\n            "name": "Laptopy 14""\n            }\n        ]\n        }
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

