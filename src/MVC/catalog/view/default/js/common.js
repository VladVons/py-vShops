"use strict"

const 
  SEARCH = '?route=product/search&search=',
  NAV = '/api/?route=product/category&method=ApiNav'

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
  
  async catalog() {
    //active menu
    let active = sessionStorage.getItem('Menu') || "{}"
    active = JSON.parse(active)
    //first level
    let menu = sessionStorage.getItem('Catalog')
    if(!menu) {
      //get from server
      let data = {}
      for(let node of $$('nav catalog')) {
        let json = await $$.post(NAV, {
          headers: {
            'Content-type': 'application/json'
          },
          body : JSON.stringify(
            {label: node.getAttribute('label')}
          )
        })
        this.menu(json, node)
        data[node.getAttribute('label')] = json
      }
      sessionStorage.setItem('Catalog', JSON.stringify(data))
    }else{
      // get from cache
      menu = JSON.parse(menu)
      for(let node of $$('nav catalog')) {
        this.menu(menu[node.getAttribute('label')], node)
      }
    }
    
    //next level
    let nodes = $$('nav catalog a')
    let toggle = async event => {
      event.returnValue = false
      let label = event.target.getAttribute('label')
      //select menu
      if(event.target.classList.contains('active')) {
        event.target.nextSibling.style.height = '0px'
        delete active[label]
      }else{
        let level = event.target
        if(event.target.classList.contains('cache')) {
          level = event.target.nextSibling
        }else{
          level = await $$.post(NAV, {
            headers: {
              'Content-type': 'application/json'
            },
            body : JSON.stringify(
              {label: label}
            )
          })
          //make node from JSON
          level = this.submenu(level)
          //append node to DOM
          if(event.target.nextSibling) {
            event.target.parentNode.insertBefore(level, event.target.nextSibling)
          }else{
            event.target.parentNode.appendChild(level)
          }
          event.target.classList.add('cache')
        }
        level.style.height = level.scrollHeight + 'px'
        active[label] = true
        //select active submenu
        let nodes = level.getElementsByTagName('a')
        for(let i=0; i<nodes.length; i++) {
          if(nodes[i].href === document.location.href) {
            wait(250).then(() => nodes[i].classList.add('view'))
          }
        }
        
      }
      //save to cache
      sessionStorage.setItem('Menu', JSON.stringify(active))
      //set class
      event.target.classList.toggle('active')
      
    }
    //set events
    for(let node of nodes) {
      if(node.getAttribute('label')) {
        node.addEventListener('click', toggle)
      }
    }
    //set active
    for(let node of nodes) {
      if(active[node.getAttribute('label')]) {
        await wait(100).then(() => {node.click()})
      }
    }
    
  }
  
  menu(json, node) {
    for(let elem of json.menu.items.data) {
      elem = Object.fromEntries(json.menu.items.head.map((key, index) => [key, elem[index]]))
      $$('<a>')
        .attr({href: elem.href, label: elem.label})
        .text(elem.name)
        .to(node)
    }
  }
  
  submenu(json) {
    let level = $$(`<level${json.menu.level}>`)[0]
    for(let elem of json.menu.items.data) {
      elem = Object.fromEntries(json.menu.items.head.map((key, index) => [key, elem[index]]))
      $$('<a>')
        .attr({href: elem.href})
        .text(elem.name)
        .to(level)
    }
    return level
  }
  
}

new Common

