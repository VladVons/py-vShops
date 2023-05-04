"use strict"

let LEGACY = !CSS.supports("container: name")

class Product {
  constructor() {
    let self = this
    $$.ready( () => {
      $$.css([
        '/default/css/optima/tip.css',
        '/default/css/1200/common.css',
        '/default/css/1200/header.css',
        '/default/css/1200/top.css',
        '/default/css/1200/menu.css',
        '/default/css/1200/page.css',
        '/default/css/1200/path.css',
        '/default/css/1200/nav.css',
        '/default/css/1200/footer.css',
        '/default/css/1200/social.css',
        '/default/css/1200/product.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
          
          //set listeners
          $$('tabs tab').on('click', self.setActive.bind(self))
          
          //set thumbs
          $$('thumbs thumb').on('click', self.setImage.bind(self))
          
          //set link for cart
          $$('control a.buy').on('click', self.toCart.bind(self))
          
        }
      )
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
    let code = item.getElementsByTagName('code')[0].getElementsByTagName('b')[0].textContent
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
        name: item.getElementsByTagName('title')[0].textContent,
        img: item.getElementsByTagName('thumb')[0].style.backgroundImage.match(/url\(['"]?([^'"]+)['"]?\)/)[1],
        count: 1,
        price: parseFloat(price.textContent)
      })
      $$.tip('Товар доданий до кошика')
    }else{
      $$.tip('Товар вже в кошику - кількість оновлена')
    }
    localStorage.setItem('Cart', JSON.stringify(data))
    event.returnValue = false
  }
  
}

window.product = new Product()
