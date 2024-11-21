Data = '''
{\n      "@context": "http://schema.org",\n      "@type": "Product",\n      \n      "description": "",\n      "name": "Komputer Dell Optiplex 7070 Micro i5-9500T 8 GB 512 SSD W11Pro A-",\n      "productID": "mpn:20910-93", \n      "brand": {\n        "@type": "Brand",\n        "name": ""Dell""\n        },\n      "image": "https://rnew.pl/hpeciai/5b6cfdb0b7bd6e36a4474bc2fc78a9cb/pol_pl_Komputer-Dell-Optiplex-7070-Micro-i5-9500T-8-GB-512-SSD-W11Pro-A-63292_1.jpg"\n      ,\n        "offers": [\n            \n            {\n            "@type": "Offer",\n            "availability": "http://schema.org/InStock",\n            "price": "1619.00",\n            "priceCurrency": "PLN",\n            "eligibleQuantity": {\n            "value":  "1",\n            "unitCode": "szt.",\n            "@type": [\n            "QuantitativeValue"\n            ]\n            },\n            "url": "https://rnew.pl/pl/products/komputer-dell-optiplex-7070-micro-i5-9500t-8-gb-512-ssd-w11pro-a-63292.html?selected_size=onesize"\n            }\n                \n        ]\n        }
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

