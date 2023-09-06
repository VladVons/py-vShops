// -= Fetch Plugin for jMagic =-
// !! [Require plugins.url] !!

"use strict";

// CONSTANTS
const 
  CLIENT = {'User-Framework': `${$$.conf.NAME}/${$$.conf.VERSION}`},
  CORE  = $$.error.CORE,
  FETCH = {
    ERR_NETWORK : {code: 10, message: 'Network Error'},
    HTTP_403: {code: 403, message: 'Access Forbidden'},
    HTTP_404: {code: 404, message: 'Not Found'},
  },
  MIME_TYPES = {
    'text/plain'                : 'text',
    'application/octet-stream'  : 'blob',
    'application/json'          : 'json',
  }


class Fetch {
  constructor() {
    // extend framework or alert
    $$.get  = (window.fetch) ? this.resolve.bind(this, 'GET') : this.reject.bind(this)
    $$.post = (window.fetch) ? this.resolve.bind(this, 'POST') : this.reject.bind(this)
    // save errors
    $$.error.FETCH = FETCH
    // Localization
    if($$.conf.lang) {
      (async () => {
        await import(`./local/${$$.conf.lang}/fetch.js`)
          .catch(msg => {$$.error({code: 1, message: msg}).as($$.error.handler)})
      })()
    }
    
  }
  
  resolve(method, path, options={}) {
    // options for request
    options.method = method
    options.headers = {...CLIENT, ...options.headers}
    this.options = options
    
    return (typeof path === 'string') 
      ? this.promise($$.url.format.apply(options, [path]))
      : Promise.all(path.map($$.url.format, options).map(this.promise.bind(this)))
  }
  
  reject() {
    return new Promise((resolve,reject) => {
      $$.error($$.error.CORE.PLUGIN).as($$.error.handler)
    })
  }
  
  promise(url) {
    return new Promise((resolve, reject) => {
      fetch(new Request(url, this.options))
        .then(response => {
          if(response.ok) {
            // HTTP-status in 200...299
            response.text()
              .then(text => {
                let mime = response.headers.get('Content-Type') || 'text/plain'
                resolve((MIME_TYPES[mime.split(';')[0]] === 'json') ? JSON.parse(text) : text)
              })
              .catch(error => {
                // JSON Parse Error
                CORE.JSON.message = error.message
                $$.error(CORE.JSON).as($$.error.handler)
              })
          }else{
            $$.error(FETCH[`HTTP_${response.status}`]).as($$.error.handler)
          }
        })
        .catch(error => {
          // Network Error
          $$.error(FETCH.ERR_NETWORK)
        })
    })
  }
}

new Fetch