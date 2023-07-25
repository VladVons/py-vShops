#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, json

print('Content-type: application/json\n')

params = json.loads(sys.stdin.read(int(os.environ['CONTENT_LENGTH'])))

label = params['label']
level = len(label.split('.'))

DATA = {
  "catalog": [
    ["Аксесуари для ноутбуків", "#", "catalog.laptop_accessories"],
    ["Кабелі та перехідники", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Комп`ютери, ноутбуки", "#", "catalog.laptop_accessories"],
    ["Комплектуючі", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Мережеве обладнання", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Носії інформації", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Периферія, аксесуари", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Планшети та аксесуари", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Різне", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Розхідні матеріали для друку", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Серверне обладнання", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Торгове обладнання", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Чистячі засоби", "#", "catalog.laptop_accessories"]
  ],
  "services": [
    ["Ремонт комп'ютерів", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Ремонт ноутбуків", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Встановлення, відновлення операційної системи Window, LINUX", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Збір системного блока комп'ютера за критеріями клієнта", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Чистка ноутбука чи комп'ютера", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Заправка картриджів", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Вічний картридж", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Ремонт принтерів", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Віддалений системний адміністратор", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Налаштування віддаленого робочого місця", "?route=product/category&path=0_1002&tenant=1", ""],
    ["1С - cупровід і консультації", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Налаштування обладнання МікроТік", "?route=product/category&path=0_1002&tenant=1", ""]
  ],
  "level": [
    ["Зарядні пристрої для ноутбуків", "?route=product/category&path=0_1001&tenant=1", ""],
    ["Охолоджуючі підставки для ноутбуків", "?route=product/category&path=0_1002&tenant=1", ""],
    ["Сумки для ноутбуків", "?route=product/category&path=0_1003&tenant=1", ""]
  ]
}

JSON = {
  "menu" : {
    "lang"  : "ua",
    "level" : level,
    "label" : label,
    "items"  : {
      "head"  : ["name", "href", "label"],
      "data"  : []
    }
  },
  "lang" : {
    "order" : "замовлення",
    "sort"  : "сортувати"
  }
}

if label == 'catalog':
  JSON["menu"]["items"]["data"] = DATA["catalog"]
elif label == 'services':
  JSON["menu"]["items"]["data"] = DATA["services"]
else:
  JSON["menu"]["items"]["data"] = DATA["level"]


print(json.dumps(JSON))
