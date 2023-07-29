"use strict"

// jMagic imports
await $$.import(['plugins.scss','plugins.telegram'])

// User imports
import {conf} from './conf.js'
import('./common.js')

class Confirm {
  constructor() {
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/cart.css`])
      $$.css(SCSS.dump(rules))
      
      //load localisation
      let lang = await $$.get(conf.url.local)
      this.lang = lang.confirm
      
      // global title
      $$('head title').text(this.lang.title)
      //unmask page
      $$('body').css({opacity: 1})
      
      //set submit
      $$('buttons button.checkout').on('click', this.submit.bind(this))
      
      //autofill form
      let client = localStorage.getItem('Client')
      if(client) {
        client = JSON.parse(client)
        $$('confirm client input')[0].value = client.name
        $$('confirm phone input')[0].value = client.phone
      }
    })
  }
  
  async submit() {
    let self = this
    let date = new Date().toLocaleString('uk-UA')
    let client = $$('confirm client input')[0]
    let phone = $$('confirm phone input')[0]
    let sum = $$('total sum')[0].textContent
    client = client.value = client.value.trim()
    phone = phone.value = phone.value.trim()
    
    //check client && phone
    if(!/^\p{L}{2,12}$/u.test(client)) {
      $$.tip(this.lang.tip.errorName)
      $$('confirm client input')[0].select()
      return false
    }
    if(!/^0(39|50|63|66|67|68|91|92|93|94|95|96|97|98|99|)\d{7}$/.test(phone)) {
      $$.tip(this.lang.tip.errorPhone)
      $$('confirm phone input')[0].select()
      return false
    }
    if(!parseFloat(sum)) {
      $$.tip(this.lang.tip.emptyBacket)
      return false
    }
    
    //save client and phone to cache
    localStorage.setItem('Client', JSON.stringify({
      name: client,
      phone: phone
    }))
    
    //get order id (oid)
    $$.mask()
    let json = await $$.post($$.url.format(conf.url.order_id), {
        headers: {
          'Content-type' : 'application/json'
        },
        body: JSON.stringify({
          cart: JSON.parse(localStorage.getItem('Cart')), 
          payment: JSON.parse(localStorage.getItem('Payment')).type,
          client: client,
          phone: phone
        })
      })
      .catch(error => {$$.tip(this.lang.tip.errorOrder)})
    
    let url = $$.url.format('/history.shtml', {order_id: json.order_id})
    let msg = 
      `Отримано нове замовлення - <a href='${url}'><b>${json.order_id}</b></a>\n`+
      `Замовник: <b>${client}</b>, телефон: <b>${phone}</b>`
    
    //send telegram message
    $$.telegram.send(msg)
      .then(result => {
        console.log(result) //JSON from Telegram
        //set tip
        sessionStorage.setItem('Tip', this.lang.tip.confirmOrder)
        // move Cart to History
        self.history(json.order_id, client, phone, date)
        //redirect to catalog
        wait(2*1000, url)
          .then(href => document.location.href = href)
      })
      .catch(error => {
        console.log(error)
        $$.tip(this.lang.tip.errorTelegram)
      })
  }
  
  history(oid, client, phone, date) {
    let cart = JSON.parse(localStorage.getItem('Cart'))
    let pay  = JSON.parse(localStorage.getItem('Payment'))
    localStorage.removeItem('Cart')
    localStorage.removeItem('Payment')
    localStorage.setItem('History', JSON.stringify([{
      date  : date,
      oid   : oid,
      client  : client,
      phone : phone,
      cart  : cart,
      pay   : pay,
      total : $$('total sum')[0].textContent,
      promo : 0,
      stat  : [{
        date : date,
        mess : this.lang.status.waitContact
      }]
    }]))
  }
  
}

new Confirm

