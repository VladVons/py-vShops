Data = '''
{\n\t\t\t"@context": "http://schema.org",\n\t\t\t"@type": "BreadcrumbList",\n\t\t\t"itemListElement": [\n\t\t\t{\n\t\t\t"@type": "ListItem",\n\t\t\t"position": 1,\n\t\t\t"item": "https://greencomputers.pl/pl/menu/laptopy-poleasingowe-100",\n\t\t\t"name": "LAPTOPY POLEASINGOWE"\n\t\t\t}\n\t\t,\n\t\t\t{\n\t\t\t"@type": "ListItem",\n\t\t\t"position": 2,\n\t\t\t"item": "https://greencomputers.pl/pl/menu/wielkosc-ekranu-192",\n\t\t\t"name": "WIELKOŚĆ EKRANU"\n\t\t\t}\n\t\t,\n\t\t\t{\n\t\t\t"@type": "ListItem",\n\t\t\t"position": 3,\n\t\t\t"item": "https://greencomputers.pl/pl/menu/od-13-do-13-9-194",\n\t\t\t"name": "od 13" do 13,9""\n\t\t\t}\n\t\t]\n\t\t}
'''
with open('RowValue.txt', 'w') as F:
    F.write(Data)

