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
  css(urls, callback) {
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

}

let $Ext = new $ExtClass
