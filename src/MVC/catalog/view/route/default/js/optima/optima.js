// framework library
// [this]: object with selected dom nodes)
class $Optima {
  // set text
  text(content) {
    for(let i=0; i<this.length; i++) {
      this[i].textContent = content
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
  // append nodes to node
  append(selector) {
    let instance = $$(selector)
    for(let i=0; i<this.length; i++) {
      for(let j=0; j<instance.length; j++) {
        this[i].appendChild(instance[j])
      }
    }
  }
}
