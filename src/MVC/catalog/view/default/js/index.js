"use strict"

// jMagic imports
await $$.import('plugins.scss')


// User imports
import('./common.js')

const 
  TITLE = 'ОСТЕР: головна'


class Index {
  constructor() {
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/index.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
      //unmask page
      $$('body').css({opacity: 1})
      
      // banner event
      $$('banner.alert')
        .on('click', event => {$$.tip('Згідно вимог чинного законодавства')})
      
    })
  }
}

new Index

