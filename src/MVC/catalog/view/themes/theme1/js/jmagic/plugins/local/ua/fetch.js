// Ukrainian language for fetch.js plugin for jMagic
// Українська мова для розширення fetch.js від jMagic 

"use strict"

const
  FETCH = {
    ERR_NETWORK: 'помилка мережі під час отримання ресурсу',
    HTTP_403: 'доступ заборонено',
    HTTP_404: 'ресурс не знайдено на сервері',
  }

// set localization
$$.error.init('FETCH', FETCH)