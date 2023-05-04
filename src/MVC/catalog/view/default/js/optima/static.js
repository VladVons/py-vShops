"use strict"

const TYPE_NOT_SUPPORTED = {code: 100, message: 'type not supported for loading'}

// extensions class
// [this]: this class
class $ExtClass {
  constructor(){
		Object
    	.getOwnPropertyNames(Object.getPrototypeOf(this))
      .filter(prop => prop !== 'constructor')
      .forEach(prop => { $$[prop] = this[prop] })
    //internal URL parser
    $$.url = new URL(document.location.href)
    $$.url.param = $$.url.searchParams
  }
  
  css(urls, callback) {
    // load css from server
    let styles = []
    let loaded = {}
    let onload = () => {
      let stat = true
      for(let url in loaded) {
        if(!loaded[url]) {
          stat = false
          break
        }
      }
      if(!stat){
        //check again
        setTimeout(onload, 100)
      }else{
        //
        for(let i=0; i<styles.length; i++) {
          let link = document.createElement('link')
          $$('head').append(
            $$(link).attr({rel: 'stylesheet', href: styles[i]})
          )
        }
        callback()
      }
    }
    for(let i=0; i<urls.length; i++) {
      let type = urls[i].split('.').pop().toLowerCase()
      if(type == 'css'){
        loaded[urls[i]] = false
        styles.push(urls[i])
        let link = document.createElement('link')
        link.addEventListener('load', () => {
          loaded[urls[i]] = true
        })
        $$('head').append(
          $$(link).attr({rel: 'preload', href: urls[i], as: 'style'})
        )
        continue
      }
      throw new Exception(TYPE_NOT_SUPPORTED, type).toString()
    }
    setTimeout(onload, 100)
  }
  
  get() {
    // GET request to server
  }
  
  post() {
    // POST request to server
  }
  
  send() {
    // WebSocket request to server
  }
  
  tip(msg, opt) {
    let tip = $$('<tip>'+msg+'</tip>')[0]
    tip.classList.add((opt) ? opt.cls || 'x' : 'x')
    tip.on = (opt) ? opt.on || 3*1000 : 3*1000
    tip.off = (opt) ? opt.off || 1*1000 : 1*1000
    
    $$('body')[0].appendChild(tip)
    setTimeout(function(){
      tip.classList.add('x-on')
      setTimeout(function(){
        tip.classList.add('x-off')
        setTimeout(function(){
          tip.parentNode.removeChild(tip)
          tip = null
        }, tip.off)
      }, tip.on)
    },100)
  }

}

let $Ext = new $ExtClass
