"use strict"

const 
  IMPORTS = ['plugins.url', 'plugins.fetch', 'plugins.scss', 'common', 'conf'],
  PATH    = 'common/home'


class Index {
  
  constructor() {
    this.conf = {}
    this.lang = {}
  }
  
  init() {
    $$(async () => {
      //load js modules
      await $$.imports(IMPORTS)
      this.conf = $$.imports.conf.conf
      
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/index.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(this.conf.url.local, { 
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

new Index().init()

