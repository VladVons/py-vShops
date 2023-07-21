"use strict"

const 
  SEARCH = '?route=product/search&search=',
  NAV = '/api/?route=product/category&method=GetNav'

class Common {
  constructor() {
    this.num = 0
    this.sum = 0.0
    
    $$( () => {
      //cart data
      this.cart()
      
      //catalog (if exist)
      this.catalog()
      
      // set global data
      let history = this.history()
      $$('top info num').text(this.num)
      $$('top info sum').text(`${this.sum.toFixed(2)} грн`)
      $$('panel links a.icon-basket num').text(this.num || '0')
      $$('panel links a.icon-ok num').text(history)
      $$('panel links a.icon-favorite num').text('0')
      $$('panel links a.icon-compare num').text('0')
      
      //search
      $$('input.search').on('keypress', (event) => {
        if(event.keyCode == 13 && event.target.value.length >= 3) {
          document.location.href = SEARCH + encodeURI(event.target.value)
        }
      })
      $$('button.search').on('click', (event) => { 
        let input = $$('input.search')[0]
        if(input.value.length >= 3) {
          document.location.href = SEARCH + encodeURI(input.value)
        }
      })
      // social icons
      let icons = $$('social icons')[0]
      $$('social share').on('click', (event) => {
        icons.classList.toggle('active')
      })
      $$('social icons a').on('click', (event) => {
        icons.classList.toggle('active')
        return false
      })
      window.addEventListener('scroll', event => {
        if(icons.classList.contains('active')) {
          icons.classList.toggle('active')
        }
      })
      //copyright
      $$('footer copyright')[0].textContent += ` (powered by jMagic/${$$.conf.VERSION})`
      
      //total data for cart
      $$('content total num').text(this.num)
      $$('content total sum').text(`${this.sum.toFixed(2)} грн`)
      $$('content total pay').text(this.pay.text)
      
    })
  }
  
  cart() {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : []
    for(let elem of data) {
      this.num++
      this.sum+=elem.count * parseFloat(elem.price)
    }
    let pay = localStorage.getItem('Payment')
    this.pay = (pay) ? JSON.parse(pay) : {type: 'cash', text: 'cash'}
  }
  
  history() {
    let store = localStorage.getItem('History')
    let data = (store) ? JSON.parse(store) : []
    return data.length
  }
  
  catalog() {
    let nodes = $$('nav catalog a')
    let toggle = async event => {
      event.returnValue = false
      if(event.target.classList.contains('active')) {
        event.target.nextSibling.style.height = '0px'
      }else{
        let level = event.target
        if(event.target.classList.contains('cache')) {
          level = event.target.nextSibling
        }else{
          level = await $$.post(NAV, {params: {level2: event.target.getAttribute('level2')}})
          level = $$(level.trim())[0]
          if(event.target.nextSibling) {
            event.target.parentNode.insertBefore(level, event.target.nextSibling)
          }else{
            event.target.parentNode.appendChild(level)
          }
          event.target.classList.add('cache')
        }
        level.style.height = level.scrollHeight + 'px'
      }
      event.target.classList.toggle('active')
    }
    for(let i=0; i<nodes.length; i++) {
      if(nodes[i].getAttribute('level2')) {
        nodes[i].addEventListener('click', toggle)
      }
    }
  }
  
}

new Common

