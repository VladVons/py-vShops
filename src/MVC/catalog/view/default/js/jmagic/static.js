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
    this.error.CORE = CORE
    // Localization
    if($$.conf.lang) {
      (async () => {
        await import(`${$$.conf.path.$$}/local/${$$.conf.lang}/jmagic.js`)
          .catch(msg => {this.error({code: 1, message: msg}).as($$.error.handler)})
      })()
    }
    $$.conf.tip.top = $$.conf.tip.top[$$.conf.DEVICE]
  }
  
  async imports(modules) {
    for(let module of modules) {
      if(module[0] === '-') continue
      let object = module
        .split('.')
        .reduce((obj, prop) => obj && obj[prop], this.imports)
      if(object) {
        console.log(`${module}: already imported!`)
      }else{
        let object = null
        let name = null
        module
          .split('.')
          .reduce((obj, prop) => {
            object = obj
            name = prop
            return obj[prop] = obj[prop] || {}
          }, this.imports)
        module = module.startsWith('plugins') 
          ? `${$$.conf.path.$$}/${module.split('.').join('/')}.js` 
          : `${$$.conf.path.js}/${module}.js`
        object[name] = await import(module)
          .catch(msg => {$$.error({code: 1, message: msg}).as($$.error.handler)})
      }
    }
  }
  
  // show tip (this - setting object)
  tip(msg) {
    let top = $$.conf.tip.top
    let opt = {cls: 'x', on: 3*1000, off: 1*1000 }
    opt = (this) ? {...opt, ...this} : opt
    opt['class'] = opt.cls
    let tip = $$(`<tip>${msg}</tip>`)
      .css({
        top: `${top}px`
      })
      .attr({...opt, top: `${top - 40}px`})
      .to(document.documentElement)[0]
    
    $$.conf.tip.top += (tip.offsetHeight + 10)
    wait(100)
      .then(async () => {
        tip.classList.add('x-on')
        await wait(tip.getAttribute('on'))
        tip.classList.add('x-off')
        tip.style.top = tip.getAttribute('top')
        await wait(tip.getAttribute('off'))
        $$.conf.tip.top -= (tip.offsetHeight + 10)
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
          message = message.split('%c(').join('<br/>(')
        }
        fn(message.split('%c').join(''))
      }
    }
  }
}

