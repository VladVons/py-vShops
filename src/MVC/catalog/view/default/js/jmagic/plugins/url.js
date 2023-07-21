// Fetch Extension for jMagic

"use strict"

export class Url {
  
  constructor() {
    this.url = new URL(document.location.href)
    this.url.params = this.params
    this.url.format = this.format
  }
  
  format(path, params) {
    let url = (/^[\.\/\?#]/.test(path))
      ? new URL(path, document.location)
      : new URL(path)
    //delete all existing parameters
    /*
    let keys = Array.from(url.searchParams.keys())
    for(let key of keys) {
      url.searchParams.delete(key)
    }
    */
    //append new parameters
    for(let key in this.params) {
      url.searchParams.append(key, this.params[key])
    }
    for(let key in params) {
      url.searchParams.append(key, params[key])
    }
    return url.href
  }
  
  params(param) {
    if(!param) {
      let query = {}
      for(let key of this.url.searchParams.keys()) {
        query[key] = this.url.searchParams.get(key)
      }
      return query
    }
    if(typeof param === 'string') {
      return this.url.searchParams.get(param)
    }
    //set params
    for(let key in param) {
      this.url.searchParams.set(key, param[key])
    }
    return this
  }
  
  go() {
    document.location.href = this.url.href
  }
  
}

$$.url = new Url