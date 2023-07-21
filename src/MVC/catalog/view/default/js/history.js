"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import('./common.js')

const 
  TITLE = 'ОСТЕР: замовлення',
  PAYMENT = {
    cash: 'готівкою',
    visa: 'карткою VISA',
    mastercard: 'карткою Mastercard',
    bitcoin: 'криптовалютою'
  }
  


class History {
  constructor() {
    
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/cart.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
      //unmask page
      $$('body').css({opacity: 1})      
      
      // cart from storage
      this.init()
      
    })
  }
  
  init() {
    let store = localStorage.getItem('History')
    let data = (store) ? JSON.parse(store) : []
    let content = $$('content')[0]
    let order_tpl = $$('template.order')[0]
    let cart_tpl = $$('template.cart')[0]
    let buts_tpl = $$('template.buttons')[0]
    for(let i=0; i<data.length; i++) {
      let order = order_tpl.content.cloneNode(true)
      let total = 0
      order.querySelector('title').textContent += data[i].order_id
      //cart data
      for(let j=0; j<data[i].cart.length; j++) {
        let cart = cart_tpl.content.cloneNode(true)
        cart.querySelector('thumb').style.backgroundImage = 'url('+data[i].cart[j].img+')'
        cart.querySelector('item a name').appendChild(document.createTextNode(data[i].cart[j].name))
        cart.querySelector('code').textContent = data[i].cart[j].code
        cart.querySelector('count').textContent = data[i].cart[j].count
        cart.querySelector('price').textContent = data[i].cart[j].price.toFixed(2)+' грн'
        cart.querySelector('sum').textContent = (data[i].cart[j].count * data[i].cart[j].price).toFixed(2)+' грн'
        total += parseFloat(data[i].cart[j].count * data[i].cart[j].price)
        while(cart.childNodes.length) {
          order.querySelector('cart').appendChild(cart.firstChild)
        }
      }
      order.querySelector('total num').textContent = data[i].cart.length
      order.querySelector('total sum').textContent = total.toFixed(2)+' грн'
      while(order.childNodes.length) {
        content.appendChild(order.firstChild)
      }
    }
    
    let buttons = buts_tpl.content.cloneNode(true)
    while(buttons.childNodes.length) {
      content.appendChild(buttons.firstChild)
    }
  }
}

new History()

