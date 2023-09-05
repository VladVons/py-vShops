"use strict"

// jMagic imports
await $$.import('plugins.scss')

const PATH = 'common/home'

// User imports
import {conf} from '../../conf.js'
import('../../common.js')

class Index {
  constructor() {
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/index.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //unmask page
      $$('body').css({opacity: 1})
      
      // banner event
      $$('banner.alert')
        .on('click', event => $$.tip(this.lang.tip_banner))
      
    })
  }
}

new Index

