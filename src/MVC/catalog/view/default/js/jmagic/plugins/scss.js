// SASS plugin for jMagic
// !! [Require plugins.fetch] !!
"use strict";

const IMPORTS = ['plugins.fetch']

class SCSSParser {
  constructor() {
    this.re = {
      comments: /\/\*[^*]*\*\//,
      extra: /\s*\n+\s*/g,
      rule: /\s*:\s*/,
      url: /(?:url\(|['"])['"]?([^'"\)]*)['"\)]+\s*(.*)/,
    }
    this.imports = []
  }
  
  Load(data) {
    let [cache, parent] = [[], []]
    let pointer = cache
    data = data
      .split(this.re.comments) //remove long comments
      .join('')
      .split(/([{}])/)        //split by blocks {}
      .filter(Boolean)
      .map(elem => {
        elem = elem.replace(this.re.extra,'').trim() //remove extra characters
        if(elem === '{') {
          parent.push(pointer)
          pointer.push([])
          pointer = pointer[pointer.length-1]
          return false
        }
        if(elem === '}') {
          let obj = this.inside(pointer) //convert block to object
          pointer = parent.pop()
          pointer.pop()
          pointer[pointer.length-1] = {selector: pointer[pointer.length-1], ...obj}
          return false
        }
        elem
          .split(';')
          .filter(Boolean)
          .map(val => pointer.push(val))
      })
    
    return this.outside(cache).flat(Infinity)
      
  }
  
  inside(data) {
    let obj = {rules: {}, children: []}
    for(let elem of data) {
      if(elem instanceof Object) {
        obj.children.push((elem instanceof Array) ? this.inside(elem) : elem) //recursion for next level
      }else{
        let [name, value] = elem.split(this.re.rule)
        if(value) {
          obj.rules[name] = value
        }else{
          obj.children.push((name[0] === '@') ? this.media(name) : name)
        }
      }
    }
    if(!Object.keys(obj.rules).length) delete obj.rules
    if(!obj.children.length) delete obj.children
    return obj
  }
  
  outside(data) {
    let cache = []
    let obj = []
    for(let elem of data) {
      if(elem instanceof Object) {
        if(cache.length) {
          obj.push({vars: Object.fromEntries(cache.map(elem => elem.split(this.re.rule)))})
          cache = []
        }
        obj.push(elem)
      }else{
        if(elem[0] === '@') {
          obj.push(this.media(elem))
        }else{
          cache.push(elem)
        }
      }
    }
    return obj
  }
  
  media(command) {
    return ({
      import: this.Import.bind(this),
    }[command.split(' ')[0].slice(1)](command))
  }
  
  Import(elem) {
    let data = elem
      .replace(/^@import\s+/,'')
      .match(this.re.url)
      .slice(1)
    this.imports.push(data[0])
    return {command: '@import', url: data[0], conditions: data[1]}
  }
  
  parse(data) {
    this.imports = []
    let parsed = this.Load(data)
    return [parsed, this.imports]
  }
}


class SCSS extends SCSSParser {
  constructor() {
    super()
    this.recursion = 0
    this.indent = 0
    window.SCSS = this
  }
  
  import(data, imp, source) {
    return data
      .map(elem => {
        if(elem.command && elem.command === '@import') {
          return source[imp.indexOf(elem.url)]
        }
        if(elem.children) {
          elem.children = this.import(elem.children, imp, source).flat(1)
        }
        return elem
      }).flat(1)
  }
  
  async load(url) {
    url = (typeof url === 'string') ? [url] : url
    let data = await $$.get(url)
    let imp = []
    for(let i=0; i<data.length; i++) {
      [data[i], imp] = super.parse(data[i])

      let base = url[i]
        .split('/')
        .slice(0,-1)
        .join('/')
      let urls = imp.map(name => `${base}/${name}`)
      
      if(imp.length) {
        this.recursion++
        let source = await this.load(urls)
        this.recursion--
        data[i] = this.import(data[i], imp, source)
      }
      
    }
    return (this.recursion) ? data : data.flat(Infinity)
  }
  
  dump(data, zip=true) {
    return data
      .map(elem => {
        if(elem.selector) {
          let prop = []
          for(let key in elem.rules) {
            prop.push((zip) ? `${key}:${elem.rules[key]};` : `  ${key}: ${elem.rules[key]};`)
          }
          if(elem.children) {
            this.indent += '  '
            prop.push(this.dump(elem.children, zip))
            this.indent = this.indent.slice(2)
          }
          
          return (zip) 
            ? `${elem.selector}{${prop.join('')}}` 
            : `${this.indent}${elem.selector} {\n${this.indent + prop.join('\n'+this.indent)}\n${this.indent}}`
        }else{
          return ''
        }
      })
      .join((zip) ? '' : '\n\n')
  }
}


new SCSS