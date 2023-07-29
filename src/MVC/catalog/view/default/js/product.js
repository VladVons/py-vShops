"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import('./common.js')

const
  TITLE = 'ОСТЕР: про товар'

class Product {
  constructor() {
    let self = this
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/product.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
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
    let data = (store) ? JSON.parse(store) : []
    let item = event.target
    while(item.nodeName.toUpperCase() != 'ITEM'){
      item = item.parentNode
    }
    //check if exist
    let exist = false
    let code = item.getAttribute('code')
    let pid = item.getAttribute('pid')
    let price = item.getElementsByTagName('price')
    price = (price.length) ? price[0] : item.getElementsByTagName('promo')[0]
    for(let product of data){
      if(product.code == code){
        product.count++
        exist = true
        break
      }
    }
    
    if(!exist) {
      data.push({
        code: code,
        pid: pid,
        name: item.getElementsByTagName('title')[0].textContent,
        img: item.getElementsByTagName('thumb')[0].style.backgroundImage.match(/url\(['"]?([^'"]+)['"]?\)/)[1],
        url: document.location.href,
        count: 1,
        price: parseFloat(price.textContent)
      })
      $$.tip('Товар доданий до кошика')
    }else{
      $$.tip('Товар вже в кошику - кількість оновлена')
    }
    localStorage.setItem('Cart', JSON.stringify(data))
    event.returnValue = false
    
    //calculate new sum
    let sum = 0.0
    for(let elem of data) {
      sum+=elem.count * parseFloat(elem.price)
    }    
    //update cart button
    $$('top info num').text(data.length)
    $$('top info sum').text(sum + ' грн')
    $$('panel links a.icon-basket num').text(data.length)
    
  }
  
}

new Product()
