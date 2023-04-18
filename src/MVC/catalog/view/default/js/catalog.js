"use strict"

let LEGACY = !CSS.supports("container: name")
import {Pages} from './pages.js'

class Catalog {
  constructor() {
    let self = this
    $$.ready( () => {
      $$.css([
        '/default/css/1200/common.css',
        '/default/css/1200/header.css',
        '/default/css/1200/top.css',
        '/default/css/1200/menu.css',
        '/default/css/1200/page.css',
        '/default/css/1200/path.css',
        '/default/css/1200/nav.css',
        '/default/css/1200/footer.css',
        '/default/css/1200/social.css',
        '/default/css/1200/catalog.css',
        '/default/css/1200/pages.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
          self.pages = new Pages({width:50, margin:20})
          
          //set selectors and his listeners
          let select = $$('select')
          for(let i=0; i<select.length; i++) {
            if($$.url.param.get(select[i].id)) {
              self.setValue(select[i])
            }
            select[i].addEventListener('change', self.setParam.bind(self))
          }
      
          // list view for old browsers
          self.setMode((LEGACY) ? 'list' : 'grid', null)
          
          // calculate pagination
          self.pages.init()
        }
      )
    })
  }
  
  setMode(mode, mess) {
    if(LEGACY && mess) {
      alert('Режим перегляду не підтримується броузером!')
      return false
    }
    let active = 'linear-gradient(to bottom, #eee, #fff)'
    let passive = 'linear-gradient(to bottom, #eee, #ccc)'
    let buts = $$('control mode')
    for(let i=0; i<buts.length; i++) {
      let styles = window.getComputedStyle(buts[i], null)
      let back = styles['background-image'].split(/,\s+/)
      buts[i].style.backgroundImage = [back[0], (mode == buts[i].className) ? active : passive].join(', ')
    }
    $$('grid')[0].className = mode
  }
  
  setParam(event) {
    $$.url.param.set(event.target.id, event.target.value)
    document.location.href = $$.url.href
  }
  
  setValue(select) {
    let value = $$.url.param.get(select.id)
    for(let i=0; i<select.length; i++) {
      if(value == select[i].value) {
        select[i].selected = true
        break
      }
    }
  }

}

window.catalog = new Catalog()
