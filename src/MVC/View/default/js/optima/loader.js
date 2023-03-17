"use strict"
const $P = new DOMParser

// main class of framework
class $Loader {
  // framework constructor
  constructor() {
    let self = this
    this.fn = function(selector, context) {
      // selector is html string
      if(selector[0] == '<' && selector.slice(-1) == '>'){
        return self.parse.apply(this, [selector, 'text/html'])
      }
      // selector is css string
      if(typeof selector === 'string') {
        return self.select.apply(this, [selector])
      }
      // selector is node
      if(selector instanceof HTMLElement) {
        return self.element.apply(this, [selector])
      }
      // selector is instance
      if(selector instanceof Object) {
        return self.extract.apply(this, [selector])
      }
    }
    this.fn.prototype = Object.getPrototypeOf(new $Optima)
    window.$$ = this.instance.bind(this)
    window.$$.ready = this.ready
  }
  
  // new optima instance
  instance(selector, context) {
    return new this.fn(selector, context)
  }
  
  // selector is html string
  parse(selector, mimeType) {
    const html = $P.parseFromString(selector, mimeType)
    this.length = 0
    html.body.childNodes.forEach((node, index) => {
      this[index] = node
      this.length = ++index
    })
    return this
  }
  
  // selector is css string
  select(selector) {
    let nodes = []
    try {
      nodes = document.querySelectorAll(selector)
    } catch(_) {
      this.length = 0
    }
    nodes.forEach(
      (node, index) => { 
        this[index] = node
        this.length = ++index 
      }
    )
    return this
  }
  
  // selector is node
  element(selector) {
    this[0] = selector
    this.length = 1
    return this
  }
  
  // selector is instance
  extract(selector) {
    for(let i=0; i<selector.length; i++){
      this[i] = selector[i]
      this.length = ++i
    }
    return this
  }
  
  // ready for use
  ready(callback) {
    // readyState: loading|interactive|complete
    if(document.readyState === "loading") {
      document.addEventListener('DOMContentLoaded', callback)
    }else{
      window.addEventListener('load', callback) // 'DOMContentLoaded' was fired, wait load event
    }
  }
}

// exception class of framework
class Exception {
  constructor(exc, value) {
    this.value = value
    this.code = exc.code
    this.message = exc.message
  }
  toString() {
    return this.message
  }
}

// initialisation of framework
new $Loader
