"use strict"

// User imports
import {conf} from './conf.js'
import('./search.js')


export class Common {
  constructor() {
    this.num = 0
    this.sum = 0.0
    
    $$( () => {
      //mobile menu
      if($$.conf.DEVICE === 'mobile') this.mobile()
      
      //setting (language/currency/palette)
      $$('panel links a.icon-settings, header panel lang, header panel currency, settings button')
        .on('click', event => {
          event.returnValue = false
          $$('settings')[0].classList.toggle('active')
        })

      //get dpi (temparary function)
      let dpi = (function () {
        for (var i = 56; i < 2000; i++) {
          if (matchMedia("(max-resolution: " + i + "dpi)").matches === true) {
            return i;
          }
        }
        return i;
      })()
      
      //cart data
      this.cart()
      
      //catalog (if exist)
      this.catalog()
      
      // set global data
      let history = this.history()
      $$('top info num').text(this.num)
      $$('top info sum').text(`${this.sum.toFixed(2)} грн`)   //!!!!!!!!!!!!!!!!!! lang
      $$('panel links a.icon-basket num').text(this.num || '0')
      $$('panel links a.icon-ok num').text(history)
      $$('panel links a.icon-favorite num').text('0')
      $$('panel links a.icon-compare num').text('0')

      // social icons
      let icons = $$('social icons')[0]
      $$('social share')
        .on('click', (event) => {
          icons.classList.toggle('active')
        })
      $$('social icons a')
        .on('click', (event) => {
          icons.classList.toggle('active')
          return false
        })
      $$('social callback')
        .on('click', event => {
          $$.mask()
          $$('popup')
            .css({opacity: 1})[0]
            .classList.toggle('active')
        })
      // popup event
      $$('popup')
        .on('transitionend', event => {
          if(event.propertyName === 'height' && event.target.clientHeight) {
            for(let node of $$('popup close, popup content')) {
              node.classList.toggle('active')
            }
          }
        })
      $$('popup close')
        .on('click', event => {
          for(let node of $$('popup close, popup content')) {
            node.classList.remove('active')
          }
          event.target.parentNode.classList.toggle('active');
          $$.unmask()
        })
        
      
      //scroll window event
      window.addEventListener('scroll', event => {
        if(icons.classList.contains('active')) {
          icons.classList.toggle('active')
        }
      })
      //copyright
      $$('footer copyright')[0].innerHTML += `<mobile><br/></mobile> (powered by jMagic/${$$.conf.VERSION})`
      
      //total data for cart
      $$('content total num').text(this.num)
      $$('content total sum').text(`${this.sum.toFixed(2)} грн`)
      $$('content total pay').text(this.pay.text)
      
    })
  }
  
  struc(data) {
    return data.head.reduce((obj, key, idx) => {
      obj[key] = idx
      return obj
    }, {})
  }
  
  cart() {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : conf.cart
    let struc = this.struc(data)
    for(let elem of data.data) {
      this.num++
      this.sum+=elem[struc.qty] * elem[struc.price]
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
    let path = $$.url.params('path')
    let active = path ? path.split('_').slice(0,2) : []
    active = active.length == 2 ? active.join('_') : null
    //first level
    let menu = sessionStorage.getItem('Catalog')
    if(!menu) {
      //get from server
      let json = await $$.post(conf.url.menu, {
        headers: {
          'Content-type': 'application/json'
        },
        body : JSON.stringify(
          {label: $$('nav catalog')[0].getAttribute('label')}
        )
      })
      this.menu(json.menu, $$('nav catalog')[0])
      // save to cache
      if(Object.keys(json).length) {
        sessionStorage.setItem('Catalog', JSON.stringify(json.menu))
      }else{
        sessionStorage.removeItem('Catalog')
      }
    }else{
      // get from cache
      this.menu(JSON.parse(menu), $$('nav catalog')[0])
    }
    
    //next level
    let nodes = $$('nav catalog a')
    let toggle = async event => {
      event.returnValue = false
      let label = event.target.getAttribute('label')
      //select menu
      if(event.target.classList.contains('active')) {
        event.target.nextSibling.style.height = '0px'
        active = null
      }else{
        let level = event.target
        if(event.target.classList.contains('cache')) {
          level = event.target.nextSibling
        }else{
          level = await $$.post(conf.url.menu, {
            headers: {
              'Content-type': 'application/json'
            },
            body : JSON.stringify(
              {label: label}
            )
          })
          //make node from JSON
          level = this.submenu(level.menu)
          //append node to DOM
          if(event.target.nextSibling) {
            event.target.parentNode.insertBefore(level, event.target.nextSibling)
          }else{
            event.target.parentNode.appendChild(level)
          }
          event.target.classList.add('cache')
        }
        level.style.height = level.scrollHeight + 'px'
        //select active submenu
        let nodes = level.getElementsByTagName('a')
        for(let i=0; i<nodes.length; i++) {
          if(nodes[i].href === document.location.href) {
            wait(250).then(() => nodes[i].classList.add('view'))
          }
        }
        
      }
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
      if(node.getAttribute('label') === active) {
        await wait(100).then(() => {node.click()})
      }
    }
  }
  
  menu(json, node) {
    for(let elem of json.items.data) {
      elem = Object.fromEntries(json.items.head.map((key, index) => [key, elem[index]]))
      $$('<a>')
        .attr({href: elem.href, label: elem.label})
        .text(elem.name)
        .to(node)
    }
  }
  
  submenu(json) {
    let level = $$(`<level${json.level}>`)[0]
    for(let elem of json.items.data) {
      elem = Object.fromEntries(json.items.head.map((key, index) => [key, elem[index]]))
      $$('<a>')
        .attr({href: elem.href})
        .text(elem.name)
        .to(level)
    }
    return level
  }

  async mobile() {
    //left swipe main menu
    let swipe = await import('./swipe.js')
    new swipe.Swipe($$('menu')[0])
    
    $$('border.menu')
      .on('click', event => {
        $$('menu').css({left: 0})
      })
    
    //fix path
    $$('path').css({display: 'block'})
    //swap path with nav
    $$('page flex nav').append($$('page path')[0])
    //nav expand catalog
    $$('nav title')
      .on('click', event => {
        let catalog = event.target
        while(catalog.nextSibling.nodeName !== 'CATALOG') {
          catalog = catalog.nextSibling
        }
        catalog = catalog.nextSibling
        catalog.style.height = (catalog.classList.contains('active')) ? 0 : catalog.scrollHeight + 'px'
        catalog.classList.toggle('active')
      })
  }
  
}

window.common = new Common

