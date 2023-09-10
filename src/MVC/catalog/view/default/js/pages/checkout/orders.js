"use strict"

const 
  IMPORTS = ['plugins.url', 'plugins.fetch', 'plugins.scss', '-common', 'conf'],
  PATH    = 'checkout/orders'


class Orders {
  constructor() {
    $$(async () => {
      //load js modules
      await $$.imports(IMPORTS)
      this.conf = $$.imports.conf.conf  //!!!!!!!!!
      
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/cart.css`])
      $$.css(SCSS.dump(rules))
      
      //unmask page
      $$('body').css({opacity: 1})      
      
      // cart from storage
      //this.init()
      
      //mobile layout
      if($$.conf.DEVICE === 'mobile') this.mobile()
      
      //show tip first time
      let tip = sessionStorage.getItem('Tip')
      if(tip) {
        $$.tip(tip)
        sessionStorage.removeItem('Tip')
      }
    
    })
  }
  
  mobile() {
    let items = $$('cart item')
    for(let item of items) {
      item.insertBefore(item.querySelector('code'), item.querySelector('price'))
    }
  }
}

new Orders
