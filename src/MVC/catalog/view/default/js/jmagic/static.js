"use strict"

const
  CORE = {
    PLUGIN : {code: 2, message: 'Plugin Not Supported'},
    JSON   : {code: 3, message: 'JSON Parse Error'},
  }

// extensions class
// [this]: this class
export class Static {
  
  constructor(){
    // initial tips
    $$('<link/>')
      .attr({rel: 'stylesheet', href: `${$$.conf.path.$$}/css/jmagic.css`})
      .to('head')
    // try for localisation
    this.error.CORE = CORE
    if($$.conf.lang) {
      $$.import(`./local/${$$.conf.lang}/jmagic`)
    }
    
  }
  
  static top = 30
  
  async import(module) {
    // relative path from self
    module = (typeof module === 'string') ? [module] : module
    for(let mod of module) {
      let imp = await import(`${$$.conf.path.$$}/${mod.replaceAll('.','/')}.js`)
        .catch(msg => {this.error({code: 1, message: msg}).as($$.error.handler)})
    }
  }

  static cache = {
    init : () => {
      let Cache = sessionStorage.getItem('Cache')
      this.cache.data.CSS = (Cache) ? JSON.parse(Cache).CSS : []
      return this.cache
    },
    data : {
      CSS : []
    },
    get : url => {
      for(let elem of this.cache.data.CSS) {
        if(url === elem.url) {
          return elem.data
        }
      }
      return null
    },
    set : elem => {
      this.cache.data.CSS.push(elem)
    },
    save : () => {
      sessionStorage.setItem('Cache', JSON.stringify(this.cache.data))
    }
  }

  // show tip
  tip(msg) {
    let top = Static.top
    let opt = {cls: 'x', on: 3*1000, off: 1*1000 }
    opt = (this) ? {...opt, ...this} : opt
    opt['class'] = opt.cls
    let tip = $$(`<tip>${msg}</tip>`)
      .css({
        top: `${Static.top}px`
      })
      .attr({...opt, top: `${Static.top - 40}px`})
      .to(document.documentElement)[0]
    
    Static.top += (tip.offsetHeight + 10)
    wait(100)
      .then(async () => {
        tip.classList.add('x-on')
        await wait(tip.getAttribute('on'))
        tip.classList.add('x-off')
        tip.style.top = tip.getAttribute('top')
        await wait(tip.getAttribute('off'))
        Static.top -= (tip.offsetHeight + 10)
        tip.parentNode.removeChild(tip)
      })
  }

  // append css data to document
  css(data) {
    $$('<style>')
      .attr({rel: 'stylesheet'})
      .text(data)
      .to('head')
  }
  
  // mask page with/without logo
  mask(logo = false) {
    let node = $$(`<mask class='global'>`)
      .to(document.documentElement)
    wait(100, 'active')
      .then(cls => {
        node[0].classList.toggle(cls)
        if(logo) {
          node.append(`<img src='${$$.conf.path.$$}/img/loading.svg'>`)
        }
      })
  }
  
  unmask() {
    let node = $$('mask.global')
    node[0].classList.toggle('active')
    wait(1000, node[0])
      .then(node => node.parentNode.removeChild(node))
  }
  
  // common error handler
  error(err) {
    let message = `%c[Error ${err.code}]: %c${err.message}`
    let color = ['color: #f00', 'color: #000']
    if(err.local) {
      message += ` %c(${err.local})`
      color.push('color: #09f')
    }
    console.error(message, ...color)
    return {
      as : fn => {
        if(fn.name === 'tip') {
          fn = fn.bind({cls: 'x err', on: 5*1000})
          message = message.replaceAll('%c(','<br/>(')
        }
        fn(message.replaceAll('%c',''))
      }
    }
  }
}

