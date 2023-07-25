"use strict"

// jMagic imports
await $$.import(['plugins.scss','plugins.telegram'])

// User imports
import('./common.js')

const 
  TITLE   = 'ОСТЕР: підтвердження замовлення',
  TIP_OK  = 'Замовлення прийняте! Очікуйте дзвінок для підтвердження',
  TIP_ERR = 'Помилка оформлення замовлення!',
  ORDER_ID = '/cgi/order.py'
  
class Confirm {
  constructor() {
    $$(async () => {
      //load css rules
      let rules = await SCSS.load([`${$$.conf.path.css}/common.css`,`${$$.conf.path.css}/desktop/cart.css`])
      $$.css(SCSS.dump(rules))
      
      // global title
      $$('head title').text(TITLE)
      //unmask page
      $$('body').css({opacity: 1})
      
      //set submit
      $$('buttons button.checkout').on('click', this.submit.bind(this))
    })
  }
  
  async submit() {
    let self = this
    let date = new Date().toLocaleString('uk-UA')
    let user = $$('confirm user input')[0]
    let phone = $$('confirm phone input')[0]
    let sum = $$('total sum')[0].textContent
    user = user.value = user.value.trim()
    phone = phone.value = phone.value.trim()
    
    //check user && phone
    if(!/^\p{L}{2,12}$/u.test(user)) {
      $$.tip("відсутнє, або некоректне ім'я")
      $$('confirm user input')[0].select()
      return false
    }
    if(!/^0(39|50|63|66|67|68|91|92|93|94|95|96|97|98|99|)\d{7}$/.test(phone)) {
      $$.tip('відсутній, або некоректний номер телефону')
      $$('confirm phone input')[0].select()
      return false
    }
    if(!parseFloat(sum)) {
      $$.tip('кошик порожній, очікується наповнення')
      return false
    }
    
    //get order id
    $$.mask()
    let order_id = await $$.post($$.url.format(ORDER_ID), {
        headers: {
          'Content-type' : 'application/json'
        },
        body: JSON.stringify({
          cart: JSON.parse(localStorage.getItem('Cart')), 
          payment: JSON.parse(localStorage.getItem('Payment')).type
        })
      })
      .catch(error => {$$.tip('Помилка реєстрації замовлення')})
    
    let url = $$.url.format('/history.shtml', {params: {order_id: order_id}})
    let msg = 
      `Отримано нове замовлення - <a href='${url}'><b>${order_id}</b></a>\n`+
      `Замовник: <b>${user}</b>, телефон: <b>${phone}</b>`
    
    self.history(order_id, user, phone, date)
    return false
    
    //send telegram message
    $$.telegram.send(msg)
      .then(result => {
        console.log(result) //JSON from Telegram
        $$.tip(TIP_OK)
        // move Cart to History
        self.history(order_id, user, phone, date)
        //redirect to catalog
        wait(4*1000, '/catalog.shtml')
          .then(href => document.location.href = href)
      })
      .catch(error => {
        console.log(error)
        $$.tip(TIP_ERR)
      })
  }
  
  history(id, user, phone, date) {
    let cart = JSON.parse(localStorage.getItem('Cart'))
    let pay  = JSON.parse(localStorage.getItem('Payment'))
    localStorage.removeItem('Cart')
    localStorage.removeItem('Payment')
    localStorage.setItem('History', JSON.stringify([{
      date  : date,
      order_id : id,
      user  : user,
      phone : phone,
      cart  : cart,
      pay   : pay,
      total : $$('total sum')[0].textContent,
      promo : 0,
      stat  : [{
        date : date,
        mess : 'Очікується контакт від консультанта магазину'
      }]
    }]))
  }
  
}

new Confirm

