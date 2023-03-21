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
  }
  
  // load css from server/cache
  load(url, callback) {
    let type = url.split('.').pop()
    if(type == 'css'){
      let link = document.createElement('link')
      if(callback) link.addEventListener('load', callback)
      $$('head').append(
        $$(link).attr({type: 'text/css', rel: 'stylesheet', href: url})
      )
      return true
    }
    throw new Exception(TYPE_NOT_SUPPORTED, type).toString()
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

}

let $Ext = new $ExtClass
