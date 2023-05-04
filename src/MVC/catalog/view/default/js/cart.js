"use strict"

let LEGACY = !CSS.supports("container: name")

class Cart {
  constructor() {
    $$.ready( () => {
      $$.css([
        '/default/css/optima/tip.css',
        '/default/css/1200/common.css',
        '/default/css/1200/header.css',
        '/default/css/1200/top.css',
        '/default/css/1200/menu.css',
        '/default/css/1200/page.css',
        '/default/css/1200/nav.css',
        '/default/css/1200/footer.css',
        '/default/css/1200/social.css',
        '/default/css/1200/cart.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
          // cart from storage
          this.init()
          // trash title
          $$('icon.trash')
            .attr({title:'видалити з кошика'})
            .on('click', this.removeItem.bind(this))
          // count events
          $$('count input')
            .on('focus',(event)=>{event.target.select()})
            .on('keyup',this.change.bind(this))
            .on('paste',this.change.bind(this))
          $$('count icon.minus')
            .attr({title:'зменьшити кількість'})
            .on('click',this.change.bind(this))
          $$('count icon.plus')
            .attr({title:'збільшити кількість'})
            .on('click',this.change.bind(this))
        }
      )
    })
  }
  
  init() {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : []
    let cart = $$('cart')[0]
    for(let i=0; i<data.length; i++) {
      let model = $$('model')[0].cloneNode(true)
      model.getElementsByTagName('thumb')[0].style.backgroundImage = 'url('+data[i].img+')'
      model.getElementsByTagName('name')[0].appendChild(document.createTextNode(data[i].name))
      model.getElementsByTagName('code')[0].textContent = data[i].code
      model.getElementsByTagName('input')[0].value = data[i].count
      model.getElementsByTagName('price')[0].textContent = data[i].price+'грн'
      model.getElementsByTagName('summ')[0].textContent = data[i].count*parseFloat(data[i].price)+'грн'
      while(model.childNodes.length){
        cart.appendChild(model.firstChild)
      }
    }
    this.checkTotal()
  }
  
  removeItem(event) {
    let node = event.target.parentNode
    let parent = node.parentNode
    let nodes = [node]
    let store = localStorage.getItem('Cart')
    let code = null
    while(node.previousSibling.nodeName.toUpperCase() != 'NAME') {
      nodes.push(node.previousSibling)
      node = node.previousSibling
      if(node.nodeName.toUpperCase() == 'CODE'){
        code = node.textContent
      }
    }
    nodes.push(node.previousSibling)
    node = node.previousSibling
    if(confirm(node.textContent.trim()+'\n\nВидалити з Вашого кошика?')){
      while(nodes.length) {
        parent.removeChild(nodes[0])
        nodes.shift()
      }
      //delete from store
      let store = localStorage.getItem('Cart')
      let data = (store) ? JSON.parse(store).filter(product=>{ return product.code != code }) : []      
      localStorage.setItem('Cart', JSON.stringify(data))
      $$.tip('товар видалено з кошика')
      //calculate total
      this.checkTotal()
    }
  }
  
  change(event) {
    let input = event.target.parentNode.getElementsByTagName('INPUT')[0]
    let count = parseInt(input.value)
    //check clipboard
    if(event.type === 'paste'){
      event.returnValue = false
      count = parseInt(event.clipboardData.getData('text/plain'))
      if(count>0 && count<1000){
        input.value = count
      }else{
        input.value = 1
      }
    }
    if(!count) {
      input.value = 1
    }else{
      if(count>1 &&  event.target.className == 'minus') {
        input.value--
      }
      if(count<999 && event.target.className == 'plus') {
        input.value++
      }
    }
    //update store
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : []
    let node = event.target.parentNode
    while(node.previousSibling.nodeName.toUpperCase() != 'CODE'){
      node = node.previousSibling
    }
    let code = node.previousSibling.textContent
    for(let product of data){
      if(product.code == code){
        product.count = parseInt(input.value)
        break
      }
    }
    localStorage.setItem('Cart', JSON.stringify(data))
    //calculate summ and total
    this.checkSumm(input)
    this.checkTotal()
  }
  
  checkSumm(target) {
    let node = target.parentNode
    let price = 0.0
    while(node.nextSibling.nodeName.toUpperCase() != 'SUMM'){
      node = node.nextSibling
      if(node.nodeName.toUpperCase() == 'PRICE'){
        price = parseFloat(node.textContent)
      }
    }
    node.nextSibling.textContent = (parseInt(target.value) * price).toFixed(2)+'грн'    
  }
  
  checkTotal() {
    let summ = $$('cart summ')
    let total = 0
    for(let i=0; i<summ.length; i++) {
      total += parseFloat(summ[i].textContent)
    }
    $$('total summ').text(total.toFixed(2)+'грн')
  }
  
}

window.cart = new Cart()

