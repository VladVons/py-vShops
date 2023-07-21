"use strict"
// GET plugin for Optima

const 
  AJAX_DEBUG = false,
  AJAX_NOT_SUPPORTED = {code: 200, mess: 'XMLHttpRequest not supported'},
  AJAX_CONNECT_ERROR = {code: 202, mess: 'Connect error'},
  HTTP_STATUS_ERROR = {code: 203, mess: 'HTTP status error'},
  HTTP_TIMEOUT = {code: 204, mess: 'HTTP timeout event'}


export class Get {
  constructor() {
    // extend framework or alert
    $$.get = (window.XMLHttpRequest) ? this.instance : () => {
      alert(`[ERROR]: ${AJAX_NOT_SUPPORTED.mess} (code: ${AJAX_NOT_SUPPORTED.code})`)
      throw new Exception(AJAX_NOT_SUPPORTED).console()
    }
  }
  
  instance(path, callback) {
    return new Request(path, callback)
  }
}

class Request {
  
  #headers = {};
  
  constructor(path, callback) {
    this.xhr = new XMLHttpRequest
    this.xhr.responseType = "" // text|arraybuffer|blob|document|json
    this.url = new URL($$.url)
    this.url.pathname = path
    
    // common events
    let events = [
      this.#onloadstart,
      this.#onreadystatechange,
      this.#onprogress,
      this.#onabort,
      this.#onerror,
      this.#onload,
      this.#ontimeout,
      this.#onloadend
    ]
    for(let event of events) {
      this.xhr[event.name.slice(1)] = event
    }
    
    if(typeof callback === 'function') {
      this.on('load', callback)
      this.send()
    }
    
    return this
  }
  
  attr(obj) {
    for(const key in obj) {
      this.xhr[key] = obj[key]
    }
    return this
  }

  params(obj) {
    for(const key in obj) {
      this.url.searchParams.set(key, obj[key])
    }
    return this
  }
  
  headers(obj) {
    this.#headers = obj
    return this
  }
  
  on(name, callback) {
    let self = this
    this.xhr.addEventListener(name, function() {
      callback({
        load: self.xhr.response
      }[name])
    })
    return this
  }
  
  send() {
    this.xhr.open('GET', this.url.href, true) // [async, user, pass]
    //headers
    for(const key in this.#headers) {
      this.xhr.setRequestHeader(key, this.#headers[key])
    }
    this.xhr.send(null)
  }
  
  abort() {
    this.xhr.abort()
  }

  // begin of request
  #onloadstart(event) {}
  
  // readystate was changed
  #onreadystatechange(event) {}
  
  // responseText - part of data
  #onprogress(event) {}
  
  // fired with call method abort()
  #onabort(event) {}
  
  // connect error
  #onerror(event) { 
    throw new Exception(AJAX_CONNECT_ERROR).console()
  }
  
  // successful request
  #onload(event) {
    if(this.status != 200) {
      throw new Exception(HTTP_STATUS_ERROR).console(this.status, this.statusText)
    }
  }
  
  // cancel on timeout
  #ontimeout(event) {
    alert('Server not responding. Try again or later.')
    throw new Exception(HTTP_TIMEOUT).console()
  }
  
  // the last event (after load|error|timeout|abort)
  #onloadend(event) {
    if(AJAX_DEBUG) console.log(this)
  }

}

// register plugin
new Get