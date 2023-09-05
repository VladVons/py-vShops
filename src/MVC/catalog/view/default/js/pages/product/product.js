"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import {conf} from '../../conf.js'
import {common} from '../../common.js'

const PATH = 'product/product'

class Product {
  constructor() {
    let self = this
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/product.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //mobile layout
      if($$.conf.DEVICE === 'mobile') this.mobile()
      
      //unmask page
      $$('body').css({opacity: 1})
      
      //show code on page
      $$('item info code b').Text = $$('item')[0].getAttribute('pid')

      //set listeners
      $$('tabs tab').on('click', self.setActive.bind(self))
      //set thumbs
      $$('thumbs thumb').on('click', self.setImage.bind(self))
      //set link for cart
      $$('control a.buy').on('click', self.toCart.bind(self))
          
    })
  }
  
  setActive(event) {
    let tabs = $$('tabs panel tab')
    for(let i=0; i<tabs.length; i++) {
      if(tabs[i] == event.target) {
        event.target.classList.add('active')
        $$('tabs data label.'+event.target.id)[0].classList.remove('hide')
      }else{
        tabs[i].classList.remove('active')
        $$('tabs data label.'+tabs[i].id)[0].classList.add('hide')
      }
    }
  }
  
  setImage(event) {
    $$('zoom img')[0].src = event.target.style.backgroundImage.match(/url\(['"]?([^'"]+)['"]?\)/)[1]
  }
  
  toCart(event) {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : conf.cart
    let struc = common.struc(data)
    let item = event.target
    while(item.nodeName.toUpperCase() != 'ITEM'){
      item = item.parentNode
    }
    //check if exist
    let exist = false
    for(let elem of data.data){
      if(elem[struc.code] == item.getAttribute('code')){
        exist = true
        break
      }
    }
    
    if(!exist) {
      let price = item.querySelector('promo') ? item.querySelector('promo') : item.querySelector('price')
      data.data.push([
        parseInt(item.getAttribute('code')), //code
        parseInt(item.getAttribute('pid')), //pid
        item.querySelector('title').textContent, //name
        item.querySelector('thumb').style.backgroundImage.match(/url\(['"]?([^'"]+)['"]?\)/)[1], //img
        document.location.href, //url
        parseInt(item.getAttribute('min')), //quantity
        parseFloat(price.textContent) //price
      ])
      $$.tip(this.lang.tip_item_add)
    }else{
      $$.tip(this.lang.tip_item_mod)
    }
    localStorage.setItem('Cart', JSON.stringify(data))
    event.returnValue = false
    
    //calculate new sum
    let sum = 0.0
    for(let elem of data.data) {
      sum+=elem[struc.qty] * elem[struc.price]
    }    
    //update cart button
    $$('top info num').text(data.data.length)
    $$('top info sum').text(`${sum} ${this.lang.currency_abbr}`)
    $$('panel links a.icon-basket num').text(data.data.length)
    
  }
  
  mobile() {
    //mobile layout (title-images-panel)
    let root = $$('item info')[0]
    let images = $$('item images')[0]
    images.classList.remove('desktop')
    root.insertBefore(images, $$('item info control')[0])
    root.insertBefore($$('content tabs')[0], $$('item info control')[0])
    root.insertBefore($$('item info title')[0], $$('item info panel')[0])
    root.insertBefore($$('item info panel')[0], images)
  }
  
}

new Product
