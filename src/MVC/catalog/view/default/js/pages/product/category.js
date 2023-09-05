"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import {conf} from '../../conf.js'
import {common} from '../../common.js'
import {Pages} from '../../pages.js'

const PATH = 'product/category'

class Category {
  constructor() {
    let self = this
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/category.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //unmask page
      $$('body').css({opacity: 1})

      //set selectors and his listeners
      let select = $$('page select')
      for(let i=0; i<select.length; i++) {
        if($$.url.params(select[i].id)) {
          self.setValue(select[i])
        }
        select[i].addEventListener('change', self.setParam.bind(self))
      }
      //add to cart link
      $$('a.buy').on('click', self.toCart.bind(self))
      
      // list view for old browsers
      self.setMode('grid')
      // set events for modes
      $$('control mode')
        .on('click', event => {
          self.setMode(event.target.className)
          event.returnValue = false
        })
      
      // calculate pagination
      self.pages = new Pages(
        $$.conf.DEVICE === 'desktop' ? {width:50, margin:20} : {width:30, margin:10}
      )
      self.pages.init()
    })
  }
  
  setMode(mode) {
    if($$.conf.LEGACY) {
      alert(this.lang.alert_not_supported)
      return false
    }
    let buts = $$('control mode')
    for(let i=0; i<buts.length; i++) {
      buts[i].classList[(mode === buts[i].className) ? 'add' : 'remove']('active')
    }
    $$('goods')[0].className = mode
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
  
  toCart(event) {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : conf.cart
    let struc = common.struc(data)
    let item = event.target
    //get item
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
      data.data.push([
        parseInt(item.getAttribute('code')), //code
        parseInt(item.getAttribute('pid')), //pid
        item.querySelector('name').textContent, //name
        item.querySelector('img').src, //img
        item.querySelector('name').parentNode.href, //url
        parseInt(item.getAttribute('min')), //quantity
        parseFloat(item.querySelector('price').textContent) //price
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
  
}

new Category
