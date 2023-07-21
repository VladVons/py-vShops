"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import {Pages} from './pages.js'
import('./common.js')

const 
  TITLE = 'ОСТЕР: каталог'


class Catalog {
  constructor() {
    let self = this
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/catalog.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
      //unmask page
      $$('body').css({opacity: 1})

      self.pages = new Pages({width:50, margin:20})
      
      //set selectors and his listeners
      let select = $$('select')
      for(let i=0; i<select.length; i++) {
        if($$.url.params(select[i].id)) {
          self.setValue(select[i])
        }
        select[i].addEventListener('change', self.setParam.bind(self))
      }
      //add to cart link
      $$('a.buy').on('click', self.toCart.bind(self))
      
      // list view for old browsers
      self.setMode(($$.conf.LEGACY) ? 'list' : 'grid', null)
      
      // calculate pagination
      self.pages.init()
    })
  }
  
  setMode(mode, mess) {
    if($$.conf.LEGACY && mess) {
      alert('Режим перегляду не підтримується броузером!')
      return false
    }
    let buts = $$('control mode')
    for(let i=0; i<buts.length; i++) {
      buts[i].classList[(mode === buts[i].className) ? 'add' : 'remove']('active')
    }
    $$('grid')[0].className = mode
  }
  
  setParam(event) {
    $$.url.params({[event.target.id]: event.target.value}).go()
  }
  
  setValue(select) {
    let value = $$.url.params(select.id)
    for(let i=0; i<select.length; i++) {
      if(value == select[i].value) {
        select[i].selected = true
        break
      }
    }
  }
  
  toggle(node) {
    let nodes = $$('nav catalog second')
    for(let i=0; i<nodes.length; i++) {
      nodes[i].style.height = (parseInt(nodes[i].style.height)) ? '0px' : nodes[i].scrollHeight + 'px'
    }
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
    for(let product of data){
      if(product.code == item.getAttribute('code')){
        product.count++
        exist = true
        break
      }
    }
    
    if(!exist) {
      data.push({
        code: item.getAttribute('code'),
        name: item.getElementsByTagName('name')[0].textContent,
        img: item.getElementsByTagName('img')[0].src,
        count: 1,
        price: parseFloat(item.getElementsByTagName('price')[0].textContent)
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

window.catalog = new Catalog()
