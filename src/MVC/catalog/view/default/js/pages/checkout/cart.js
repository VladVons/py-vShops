"use strict"

const 
  IMPORTS = ['plugins.url', 'plugins.fetch', 'plugins.scss', 'common', 'conf'],
  PATH    = 'checkout/cart'

class Cart {
  constructor() {
    
    $$(async () => {
      //load js modules
      await $$.imports(IMPORTS)
      this.conf = $$.imports.conf.conf
      
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/${$$.conf.DEVICE}/cart.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(this.conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //unmask page
      $$('body').css({opacity: 1})      
      
      // cart from storage
      this.init()
      
      //mobile layout
      if($$.conf.DEVICE === 'mobile') this.mobile()
      
      // select events
      $$('item cbox')
        .on('click', this.selectItem.bind(this))
      $$('titles cbox')
        .on('click', this.selectAll.bind(this))
      
      // quantity events
      $$('qty input')
        .on('focus',(event)=>{event.target.select()})
        .on('keyup',this.changeQty.bind(this))
        .on('paste',this.changeQty.bind(this))
      $$('qty minus')
        .attr({title: this.lang.title_minus})
        .on('click',this.changeQty.bind(this))
      $$('qty plus')
        .attr({title: this.lang.title_plus})
        .on('click',this.changeQty.bind(this))
      
      //payment method
      this.setPayment()
      $$('payment type')
        .on('click', this.setPayment.bind(this))
      for(let node of $$('payment type')) {
        node.setAttribute('title', this.lang[`payment_${node.className}`])
        node.textContent = this.lang[`payment_${node.className}`]
      }
      
      //set buttons events
      $$('buttons button.checkout')
        .attr({href: this.conf.url.confirm})
        .on('click', this.confirm.bind(this))
      $$('buttons button.remove')
        .on('click', this.removeItems.bind(this))
      $$('buttons button.category')
        .on('click', event => document.location.href = this.conf.url.category)
      
      //joke from CX
      $$('body')
        .on('copy', event => {event.clipboardData.setData('text/plain','ХУЙ ВАМ!'); event.preventDefault();})
      
    })
  }
  
  init() {
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : this.conf.cart
    let struc = common.struc(data)
    let cart = $$('cart')[0]
    let fragment = $$('template')[0]
    
    for(let elem of data.data) {
      let model = fragment.content.cloneNode(true)
      model.querySelector('item').setAttribute('code', elem[struc.code])
      model.querySelector('item').setAttribute('pid', elem[struc.pid])
      model.querySelector('thumb').style.backgroundImage = `url(${elem[struc.img]})`
      model.querySelector('item name a').appendChild(document.createTextNode(elem[struc.name]))
      model.querySelector('item code').textContent = elem[struc.code]
      model.querySelector('item qty input').value = elem[struc.qty]
      model.querySelector('item price').textContent = `${elem[struc.price].toFixed(2)} ${this.lang.currency_abbr}`
      model.querySelector('item sum').textContent = `${(elem[struc.qty] * elem[struc.price]).toFixed(2)} ${this.lang.currency_abbr}`
      
      //set links
      for(let item of model.querySelectorAll('item a')) {
        item.href = elem[struc.url]
      }
      
      //insert model to cart
      while(model.childNodes.length){
        cart.appendChild(model.firstChild)
      }
    }
    
    this.checkTotal()
  }
  
  selectItem(event) {
    event.target.parentNode.parentNode.classList.toggle('selected')
    for(let input of $$('item cbox input')) {
      if(!input.checked) {
        $$('titles cbox input')[0].checked = false
        return
      }
      $$('titles cbox input')[0].checked = true
    }
  }
  
  selectAll(event) {
    for(let input of $$('item cbox input')) {
      input.checked = event.target.checked ? true : false
      input.parentNode.parentNode.classList[event.target.checked ? 'add' : 'remove']('selected')
    }
  }
  
  removeItems(event) {
    //empty cart
    if(event.target.classList.contains('disabled')) {
      alert(this.lang.alert_empty_cart)
      return false
    }
    //try to remove
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : this.conf.struc
    let struc = common.struc(data)

    let items = []
    let codes = []
    for(let input of $$('item cbox input')) {
      if(input.checked) {
        items.push(input.parentNode.parentNode)
        codes.push(input.parentNode.parentNode.getAttribute('code'))
      }
    }
    if(items.length && confirm(this.lang.confirm_item_remove)) {
      while(items.length) {
        items[0].parentNode.removeChild(items.shift())
      }
      $$('titles cbox input')[0].checked = false
    }else{
      //cancel remove
      return false
    }
    //delete from store
    localStorage.setItem('Cart', JSON.stringify({
      head: data.head, 
      data: data.data.filter(item => { return !codes.includes(`${item[struc.code]}`) })
    }))
    $$.tip(this.lang.tip_item_removed)
    
    //calculate total
    this.checkTotal()
  }
  
  changeQty(event) {
    let input = event.target.parentNode.getElementsByTagName('INPUT')[0]
    let qty = parseInt(input.value)
    let min = parseInt(input.getAttribute('min'))
    let max = parseInt(input.getAttribute('max'))
    let step = parseInt(input.getAttribute('step'))
    let total = true
    
    //check clipboard
    if(event.type === 'paste'){
      event.returnValue = false
      qty = parseInt(event.clipboardData.getData('text/plain'))
      if(isNaN(qty) || qty < min) {
        qty = min
      }
      if(qty > max){
        qty = max
      }
      input.value = qty
    }
    // minus button
    if(event.target.nodeName.toUpperCase() === 'MINUS') {
      if(qty >= min + step) {
        input.value = qty - step
      }else{
        event.target.parentNode.parentNode.querySelector('cbox input').checked = true
        event.target.parentNode.parentNode.classList.add('selected')
        this.removeItems({target: $$('buttons button.remove')[0]})
        total = false
      }
    }
    //plus button
    if(event.target.nodeName.toUpperCase() === 'PLUS') {
      input.value = (qty <= max - step) ? qty + step : max
    }
    
    //update store
    let store = localStorage.getItem('Cart')
    let data = (store) ? JSON.parse(store) : this.conf.cart
    let struc = common.struc(data)
    let code = event.target.parentNode.parentNode.getAttribute('code')
    for(let product of data.data){
      if(product[struc.code] == code){
        product[struc.qty] = parseInt(input.value)
        break
      }
    }
    localStorage.setItem('Cart', JSON.stringify(data))
    //calculate summ and total
    if(total) {
      this.checkSumm(input)
      this.checkTotal()
    }
  }
  
  checkSumm(target) {
    let node = target.parentNode //qty
    let price = node.parentNode.querySelector('price')
    node.parentNode.querySelector('sum')
      .textContent = `${(parseInt(target.value) * parseFloat(price.textContent)).toFixed(2)} ${this.lang.currency_abbr}`
  }
  
  checkTotal() {
    let sum = $$('cart sum')
    let total = 0
    for(let i=0; i<sum.length; i++) {
      total += parseFloat(sum[i].textContent)
    }
    $$('total num, top info num').text(sum.length)
    $$('total sum, top info sum').text(`${total.toFixed(2)} ${this.lang.currency_abbr}`)
    $$('panel links a.icon-basket num').text(sum.length)
    //check empty
    if(!sum.length) {
      let buttons = $$('buttons button.checkout, buttons button.remove')
      for(let button of buttons) {
        button.classList.toggle('disabled')
      }
      //show empty
      $$('empty')[0].classList.toggle('hide')
    }
  }

  setPayment(event) {
    if(event) {
      for(let node of $$('payment type')) {
        if(node.className === event.target.className) {
          node.setAttribute('checked', true)
        }else{
          node.removeAttribute('checked')
        }
      }
      //update store
      localStorage.setItem('Payment', JSON.stringify(
        {type: event.target.className, text: this.lang[`payment_${event.target.className}`]}
      ))
    }else{
      let payment = localStorage.getItem('Payment')
      if(!payment) {
        payment = {type: 'cash', text: this.lang.payment_cash}
        localStorage.setItem('Payment', JSON.stringify(payment))
      }else{
        payment = JSON.parse(payment)
      }
      //set active payment type
      $$(`payment type.${payment.type}`).attr({checked: true})
    }
  }
  
  confirm(event) {
    //empty cart
    if(event.target.classList.contains('disabled')) {
      alert(this.lang.alert_empty_cart)
      return false
    }
    document.location.href = event.target.getAttribute('href')
  }
  
  mobile() {
    let items = $$('cart item')
    for(let item of items) {
      item.insertBefore(item.querySelector('cbox'), item.querySelector('price'))
      item.insertBefore(item.querySelector('code'), item.querySelector('price'))
    }
  }
  
}

new Cart()

