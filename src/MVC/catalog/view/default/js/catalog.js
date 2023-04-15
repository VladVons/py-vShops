"use strict"

let LEGACY = !CSS.supports("container: name")
import {Pages} from './pages.js'

class Catalog {
  constructor() {
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
          this.pages = new Pages({width:50, margin:20})
      
          // list view for old browsers
          catalog.setMode((LEGACY) ? 'list' : 'grid', null)
          // calculate pagination
          this.pages.init()
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
}

window.catalog = new Catalog()
