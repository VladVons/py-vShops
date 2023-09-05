"use strict"

// jMagic imports
await $$.import(['plugins.scss','plugins.telegram'])

// User imports
import {conf} from '../../conf.js'
import {common} from '../../common.js'

const PATH = 'checkout/confirm'


class Confirm {
  constructor() {
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/cart.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
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
      $$.tip(this.lang.tip_error_name)
      $$('confirm client input')[0].select()
      return false
    }
    if(!/^0(39|50|63|66|67|68|91|92|93|94|95|96|97|98|99|)\d{7}$/.test(phone)) {
      $$.tip(this.lang.tip_error_phone)
      $$('confirm phone input')[0].select()
      return false
    }
    if(!parseFloat(sum)) {
      $$.tip(this.lang.tip_empty_backet)
      return false
    }
    
    //save client and phone to cache
    localStorage.setItem('Client', JSON.stringify({
      name: client,
      phone: phone
    }))
    
    //get order_id (oid)
    $$.mask(true)
    let json = await $$.post($$.url.format(conf.url.order_id), {
        headers: {
          'Content-type' : 'application/json'
        },
        body: JSON.stringify({
          cart: self.format(JSON.parse(localStorage.getItem('Cart'))), 
          payment: JSON.parse(localStorage.getItem('Payment')).type,
          client: client,
          phone: phone
        })
      })
      .catch(error => {$$.tip(this.lang.tip_error_order)})
    
    let url = $$.url.format(conf.url.history, {order_id: json.order_id})
    let msg = 
      `Отримано нове замовлення - <a href='${url}'><b>${json.order_id}</b></a>\n`+
      `Замовник: <b>${client}</b>, телефон: <b>${phone}</b>`
    alert(msg)
    return false
    
    //send telegram message
    $$.telegram.send(msg)
      .then(result => {
        console.log(result) //JSON from Telegram
        //set tip
        sessionStorage.setItem('Tip', this.lang.tip_confirm_order)
        // move Cart to History
        self.history(json.order_id, client, phone, date)
        //redirect to catalog
        wait(2*1000, url)
          .then(href => document.location.href = href)
      })
      .catch(error => {
        console.log(error)
        $$.tip(this.lang.tip_error_telegram)
      })
  }
  
  format(json) {
    let struc = common.struc(json)
    let allowed = [struc.pid, struc.qty, struc.price]
    return {
      head: json.head.filter((el, index) => allowed.includes(index)), 
      data: json.data.map(item => {return item.filter((el, index) => allowed.includes(index))})
    }
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
        mess : this.lang.status_wait_contact
      }]
    }]))
  }
  
}

new Confirm

