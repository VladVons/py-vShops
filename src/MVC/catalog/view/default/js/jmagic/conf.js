"use strict"

// user's configuration
export const
  lang = 'ua',
  path = {
    js      : '/default/js',
    $$      : '/default/js/jmagic',
    leaflet : '/default/js/leaflet',
    css     : '/default/css',
  },
  icons = {
    hex     : emo => {
      return `\\u${emo.codePointAt(0).toString(16)}`
    },
    like      : '\u1f44d',
    dislike   : '\u1f44e',
    kiss      : '\u1f48b',
    airplane  : '\u2708',
    ukraine   : '\u1f1e6',
  }
