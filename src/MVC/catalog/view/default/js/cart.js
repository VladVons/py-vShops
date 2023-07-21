"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import('./common.js')

const 
  TITLE = 'ОСТЕР: кошик',
  PAYMENT = {
    cash: 'готівкою',
    visa: 'карткою VISA',
    mastercard: 'карткою Mastercard',
    bitcoin: 'криптовалютою'
  }
  


class Cart {
  constructor() {
    
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/cart.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
      //unmask page
      $$('body').css({opacity: 1})      
      
      // cart from storage
      this.init()
      
      // trash title
      $$('trash icon')
        .attr({title:'видалити з кошика'})
        .on('click', this.removeItem.bind(this))
      // count events
      $$('count input')
        .on('focus',(event)=>{event.target.select()})
        .on('keyup',this.change.bind(this))
        .on('paste',this.change.bind(this))
      $$('count minus')
        .attr({title:'зменьшити кількість'})
        .on('click',this.change.bind(this))
      $$('count plus')
        .attr({title:'збільшити кількість'})
        .on('click',this.change.bind(this))
      $$('body')
        .on('copy', event => {event.clipboardData.setData('text/plain','ХУЙ ВАМ!'); event.preventDefault();})
      
      //payment method
      this.setPayment()
      $$('payment icon')
        .on('click', this.setPayment.bind(this))
      $$('payment input')
        .on('click', this.setPayment.bind(this))
      
      //set checkout event
      $$('buttons button.checkout')
        .on('click', this.confirm.bind(this))
      
    })
  }
  
  init() {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : []
    let cart = $$('cart')[0]
    let fragment = $$('template')[0]
    for(let i=0; i<data.length; i++) {
      let model = fragment.content.cloneNode(true)
      model.querySelector('thumb').style.backgroundImage = 'url('+data[i].img+')'
      model.querySelector('item a name').appendChild(document.createTextNode(data[i].name))
      model.querySelector('code').textContent = data[i].code
      model.querySelector('input').value = data[i].count
      model.querySelector('price').textContent = data[i].price.toFixed(2)+' грн'
      model.querySelector('sum').textContent = (data[i].count * data[i].price).toFixed(2)+' грн'
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
    while(node.previousSibling.nodeName.toUpperCase() != 'ITEM') {
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
      if(count>1 &&  event.target.nodeName.toUpperCase() == 'MINUS') {
        input.value--
      }
      if(count<999 && event.target.nodeName.toUpperCase() == 'PLUS') {
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
    return false
  }
  
  checkSumm(target) {
    let node = target.parentNode
    let price = 0.0
    while(node.nextSibling.nodeName.toUpperCase() != 'SUM'){
      node = node.nextSibling
      if(node.nodeName.toUpperCase() == 'PRICE'){
        price = parseFloat(node.textContent)
      }
    }
    node.nextSibling.textContent = (parseInt(target.value) * price).toFixed(2)+' грн'    
  }
  
  checkTotal() {
    let sum = $$('cart sum')
    let total = 0
    for(let i=0; i<sum.length; i++) {
      total += parseFloat(sum[i].textContent)
    }
    $$('total num, top info num').text(sum.length)
    $$('total sum, top info sum').text(total.toFixed(2)+' грн')
    $$('panel links a.icon-basket num').text(sum.length)
    this.toggleButtons(sum.length)
  }

  setPayment(event) {
    if(event) {
      let node = event.target
      if(node.nodeName !== 'INPUT') {
        while(node.previousSibling.nodeName !== 'INPUT') {
          node = node.previousSibling
        }
        node.previousSibling.checked = true
        //update store
        localStorage.setItem('Payment', JSON.stringify(
          {type: node.previousSibling.value, text: PAYMENT[node.previousSibling.value]})
        )
      }else{
        localStorage.setItem('Payment', JSON.stringify({type: node.value, text: PAYMENT[node.value]}))
      }
    }else{
      let payment = localStorage.getItem('Payment')
      if(!payment) {
        payment = {type: 'cash', text: PAYMENT['cash']}
        localStorage.setItem('Payment', JSON.stringify(payment))
      }else{
        payment = JSON.parse(payment)
      }
      let input = $$('payment input')
      for(let i=0; i<input.length; i++) {
        if(input[i].value === payment.type) {
          input[i].checked = true
          break
        }
      }
    }
  }
  
  toggleButtons(num) {
    if(!num) {
      let buttons = $$('buttons button.checkout, buttons button.continue')
      for(let i=0; i<buttons.length; i++) {
        buttons[i].classList.toggle('continue')
        buttons[i].classList.toggle('checkout')
      }
      //show empty
      $$('empty')[0].classList.toggle('hide')
    }
  }
  
  confirm(event) {
    if(!parseInt($$('total num')[0].textContent)) {
      event.preventDefault();
    }else{
      document.location.href = event.target.getAttribute('href')
    }
  }
  
}

new Cart()

