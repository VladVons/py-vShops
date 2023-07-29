#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os, sys, json

print('Content-type: application/json\n')
params = os.environ['QUERY_STRING']

name, value = params.split('=')

JSON = {
  "ua" : {
    "confirm" : {
      "title"       : "ОСТЕР: підтвердження замовлення",
      "tip" : {
        "confirmOrder"  : "Замовлення прийняте. Очікуйте дзвінок для підтвердження",
        "errorOrder"    : "Помилка оформлення замовлення",
        "errorTelegram" : "Замовлення не надіслане в Телеграм",
        "errorName"     : "Відсутнє, або некоректне ім'я клієнта",
        "errorPhone"    : "Відсутній, або некоректний номер телефону",
        "emptyBacket"   : "Кошик порожній, очікується наповнення",
      },
      "status" : {
        "waitContact"   : "Очікується контакт від консультанта магазину"
      }
    }
  }
}

if name == 'lang':
  print(json.dumps(JSON[value]))
else:
  print('{"status": "error"}')