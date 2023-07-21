"use strict"

// IMPORT JMAGIC'S LIBRARIES
import * as CONF from './conf.js'
import { Library } from './library.js'
import { Static } from './static.js'

// GLOBAL CONSTANTS
const 
  NAME    = 'jMagic',
  VERSION = '0.0.1',
  LEGACY  = !CSS.supports("container: name")

// FRAMEWORK CONSTANTS
const 
  PARSER = new DOMParser

// =======================
// MAIN CLASS OF FRAMEWORK
// =======================
class jMagic {
  
  #ready = false;
  
  // framework constructor
  constructor() {
    let self = this
    window.addEventListener('load', () => { self.#ready = true } )
    
    // apply prototypes
    new Proto
    
    // MAIN FUNCTION OF FRAMEWORK
    let fn = function(selector, context) {
      //selector is string
      if(typeof selector === 'string') {
        // selector is html string
        if(selector[0] === '<' && selector.slice(-1) === '>'){
          return self.iterator(self.parse.apply(this, [selector, context, 'text/html']))
        }
        // selector is css string
        return self.iterator(self.select.apply(this, [selector, context]))
      }
      // selector is node
      if(selector instanceof HTMLElement) {
        return self.iterator(self.element.apply(this, [selector, context]))
      }
      // selector is function
      if(typeof selector === 'function') {
        // ready function
        self.ready(selector)
      }
      // selector is instance
      if(selector instanceof Object) {
        return self.iterator(self.extract.apply(this, [selector, context]))
      }
    }
    fn.prototype = Object.getPrototypeOf(new Library)
    
    window.$$ = (selector, context) => { return new fn(selector, context) }
    window.wait = $$.wait = this.wait
    
    // global constants
    $$.conf = {NAME,VERSION,LEGACY,...CONF}
    
    //static extensions
    $$.__proto__ = Static.prototype
    new Static
    
    //default error handler
    $$.error.handler = $$.tip
    
    //init localisation
    $$.error.init = (name, obj) => {
      for(let key in $$.error[name]) {
        $$.error[name][key].local = obj[key] || ''
      }
    }
    console.log($$)
  }
  
  // async wait
  async wait(ms, value) {
    return new Promise(resolve => setTimeout(resolve, ms, value))
  }
  
  // async ready
  async ready(callback) {
    while(!this.#ready) {
      await this.wait(50)
    }
    callback()
  }
  
  // selector is html string
  parse(selector, context, mimeType) {
    // first way
    const template = document.createElement('template')
    template.innerHTML = selector
    template.content.childNodes.forEach((node , index) => {
      this[index] = node
    })
    this.length = template.content.childElementCount
    return this
    
    //second way
    const html = PARSER.parseFromString(`<root>${selector}</root>`, mimeType)
    const root = html.querySelector('root')
    root.childNodes.forEach((node, index) => {
      this[index] = node
    })
    this.length = root.childNodes.length
    return this
  }
  
  // selector is css string
  select(selector, context) {
    let nodes = []
    this.length = 0
    try {
      nodes = document.querySelectorAll(selector)
    } catch(_) {
      //
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
  element(selector, context) {
    this[0] = selector
    this.length = 1
    return this
  }
  
  // selector is instance
  extract(selector, context) {
    for(let i=0; i<selector.length; i++){
      this[i] = selector[i]
      this.length = ++i
    }
    return this
  }
  
  //make iterator
  iterator(instance) {
    //unset enumerable (for..in)
    Object.defineProperty(instance, 'length', {enumerable: false, writable: true})
    //make itarable (for..of)
    instance[Symbol.iterator] = function() {
      return {
        current : 0,
        last    : instance.length,
        next() {
          return this.current < this.last ? {done: false, value: this.current++} : {done: true}
        }
      }
    }
    return instance
  }
  
}

// EXTENSIONS OF PROTOTYPES
class Proto {
  constructor() {
    String.prototype.format = function(args){
      //args - hash of params
      let text = this
      for(var attr in args){
        text = text.split('{' + attr + '}').join(args[attr]);
      }
      return text
    }
    Array.prototype.clone = function(){
      return this.slice(0)
    }
  }
}

// INITIALISATION OF FRAMEWORK
new jMagic

