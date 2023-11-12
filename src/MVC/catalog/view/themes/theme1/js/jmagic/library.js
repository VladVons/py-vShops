// framework library
// [this]: object with selected dom nodes)

export class Library {
  // delete all nodes
  reset() {
    for(let i=0; i<this.length; i++) {
      delete this[i]
    }
    this.length = 0
    return this
  }
  // set text
  text(value) {
    for(let i=0; i<this.length; i++) {
      this[i].textContent = value
    }
    return this
  }
  // set styles
  css(styles) {
    for(let i=0; i<this.length; i++) {
      for(let name in styles) {
				this[i].style[name] = styles[name]
      }
    }
    return this
  }
  // set attributes
  attr(attributes) {
    for(let i=0; i<this.length; i++) {
      for(name in attributes) {
        this[i].setAttribute(name, attributes[name])
      }
    }
    return this
  }
  // append nodes to node (RENAME TO ADD)
  append(selector) {
    let instance = $$(selector)
    for(let i=0; i<this.length; i++) {
      for(let j=0; j<instance.length; j++) {
        this[i].appendChild(instance[j])
      }
    }
  }
  // remove nodes from
  delete(selector) {
    for(let i=0; i<this.length; i++) {
      this[i].parentNode.removeChild(this[i])
      delete this[i]
      this.length--
    }
    return this
  }
  // append nodes to selector
  to(selector, position) {
    let target = $$(selector)
    for(let i=0; i<target.length; i++) {
      for(let j=0; j<this.length; j++) {
        target[i].appendChild(this[j])
      }
    }
    return this
  }
  // append event to nodes
  on(event, fn) {
    for(let i=0; i<this.length; i++) {
      this[i].addEventListener(event, fn)
    }
    return this
  }
  // search node up to dom
  up(selector) {
    let matches = []
    for(let i=0; i<this.length; i++) {
      let node = this[i]
      while(node.parentNode) {
        node = node.parentNode
        if(node.matches && node.matches(selector)) {
          matches.push(node)
          break
        }
      }
    }
    this.reset()
    for(let i=0; i<matches.length; i++) {
      this[i] = matches[i]
      this.length++
    }
    return this
  }
  // mask node as loading
  mask(text = '') {
    let i = this.length
    let clone = ['borderTopLeftRadius','borderTopRightRadius','borderBottomLeftRadius','borderBottomRightRadius',
      'borderTopWidth','borderRightWidth','borderBottomWidth','borderLeftWidth']
    
    while(i--) {
      let styles = getComputedStyle(this[i])
      let css = {
        top     : `${this[i].offsetTop}px`, 
        left    : `${this[i].offsetLeft}px`,
        width   : `${this[i].offsetWidth}px`,
        height  : `${this[i].offsetHeight}px`,
      }
      for(let prop of clone) {
        css[prop] = styles[prop]
      }
      $$(`<mask>${(text.length) ? '<text>'+text+'...</text>' : ''}</mask>`)
        .css(css)
        .to('body')
    }
    return this
  }
  //getters && setters
  get Text() {
    let text = []
    for(let i of this) {
      text.push(this[i].textContent)
    }
    return text.length ? text.length > 1 ? text : text[0] : ''
  }
  set Text(value) {
    let i = this.length
    while(i--) {
      this[i].textContent = value
    }
    return this
  }
}
