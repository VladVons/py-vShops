"use strict"

const 
  IMPORTS = ['plugins.url', 'plugins.fetch', 'plugins.scss', 'common', 'conf'],
  PATH    = 'checkout/history'


class History {
  constructor() {
    $$(async () => {
      //load js modules
      await $$.imports(IMPORTS)
      this.conf = $$.imports.conf.conf
      
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/cart.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(this.conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //unmask page
      $$('body').css({opacity: 1})      
      
      // cart from storage
      this.init()
      
      //mobile layout
      if($$.conf.DEVICE === 'mobile') this.mobile()
      
      //show tip first time
      let tip = sessionStorage.getItem('Tip')
      if(tip) {
        alert(tip)
        sessionStorage.removeItem('Tip')
      }
    
    })
  }
  
  init() {
    let store = localStorage.getItem('History')
    let data = (store) ? JSON.parse(store) : []
    let content = $$('content')[0]
    let order_tpl = $$('template.order')[0]
    let cart_tpl = $$('template.cart')[0]
    let buts_tpl = $$('template.buttons')[0]
    for(let elem of data) {
      let struc = common.struc(elem.cart)
      let order = order_tpl.content.cloneNode(true)
      let total = 0
      order.querySelector('title').textContent += elem.oid
      //cart data
      for(let item of elem.cart.data) {
        let cart = cart_tpl.content.cloneNode(true)
        cart.querySelector('a').style.backgroundImage = `url(${item[struc.img]})`
        cart.querySelector('name a').appendChild(document.createTextNode(item[struc.name]))
        cart.querySelector('code').textContent = item[struc.code]
        cart.querySelector('qty').textContent = item[struc.qty]
        cart.querySelector('price').textContent = `${item[struc.price].toFixed(2)} ${this.lang.currency_abbr}`
        cart.querySelector('sum').textContent = `${(item[struc.qty] * item[struc.price]).toFixed(2)} ${this.lang.currency_abbr}`
        total += parseFloat(item[struc.qty] * item[struc.price])
        let link = cart.querySelectorAll('item a')
        for(let x=0; x<link.length; x++) {
          link[x].href = item[struc.url]
        }
        while(cart.childNodes.length) {
          order.querySelector('cart').appendChild(cart.firstChild)
        }
      }
      order.querySelector('total num').textContent = elem.cart.data.length
      order.querySelector('total sum').textContent = `${total.toFixed(2)} ${this.lang.currency_abbr}`
      while(order.childNodes.length) {
        content.appendChild(order.firstChild)
      }
    }
    
    let buttons = buts_tpl.content.cloneNode(true)
    while(buttons.childNodes.length) {
      content.appendChild(buttons.firstChild)
    }
  }

  mobile() {
    // make title as abbr
    let qty = $$('titles title.qty')[0]
    qty.textContent = qty.dataset.abbr
    
    let items = $$('cart item')
    for(let item of items) {
      item.insertBefore(item.querySelector('code'), item.querySelector('price'))
    }
  }
}

new History

