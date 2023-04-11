"use strict"

let LEGACY = !CSS.supports("container: name")

//це також зроблю класом - буде базовий клас OSTER
$$.ready( () => {
  //завантаження стилів
  $$.load('/default/css/styles.css')
  $$.load('/default/css/desktop.css', function(){
    console.log('desktop.css loaded')
    if(PAGE == 'catalog') {
      //ініціалізація класів
      window.catalog = new Catalog()
      window.pages = new Pages({width:50, margin:20})
  
      // list view for old browsers
      catalog.setMode((LEGACY) ? 'list' : 'grid', null)
      // calculate pagination
      pages.init()
      
    }
  })
})

class Catalog {
  constructor() {
    console.log('class Catalog created')
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

class Pages {
  constructor(param) {
    this.width = param.width
    this.margin = param.margin
    this.data = $$('pages data')[0]
    this.list = $$('pages data list')[0]
    this.pages = $$('pages data list page')
    this.count = 0
    $$('pages start')[0].addEventListener('click', this.scroll.bind(this))
    $$('pages end')[0].addEventListener('click', this.scroll.bind(this))
    $$('pages left')[0].addEventListener('click', this.scroll.bind(this))
    $$('pages right')[0].addEventListener('click', this.scroll.bind(this))
    for(let i=0; i<this.pages.length; i++){
      this.pages[i].addEventListener('click', (event) => {
        document.location.hash = event.target.textContent
        document.location.reload()
      })
    }
  }
  
  init() {
    //calculate width and count
    this.data.width = this.data.clientWidth
    this.count = this.data.width / (this.width + this.margin)
    this.count = (this.data.width % this.count) ? parseInt(this.count) : this.count - 1
    let rest = this.data.width - (this.count * (this.width + this.margin)) - this.margin
    this.margin += parseInt(rest / (this.count + 1))
    this.limit = (this.pages.length-this.count)*(this.width + this.margin)
    //decrease main container
    this.data.style.marginLeft = parseInt(rest % (this.count + 1) / 2) + 'px'
    this.data.style.marginRight = (rest % (this.count + 1)) - (rest % (this.count + 1) % 2) + 'px'
    this.data.width = this.data.clientWidth
    //apply new positions
    $$('pages data list')[0].style.left = this.margin+'px'
    $$('pages data list page').css({marginRight: this.margin+'px'})
    //set active page
    this.active(parseInt(document.location.hash.slice(1)) || 1)
  }
  
  scroll(event) {
    // scroll pages without reload
    let self = this
    return ({
      start : () => { self.list.style.left = self.margin+'px'},
      end   : () => { self.list.style.left = -self.limit + self.margin+'px' },
      left  : () => { 
        let x = -parseInt(self.list.style.left) - (self.count * (self.width + self.margin))
        self.list.style.left = (x > self.margin) ? -x+'px' : self.margin+'px'
      },
      right : () => { 
        let x = -parseInt(self.list.style.left) + (self.count * (self.width + self.margin))
        self.list.style.left = (x <= self.limit) ? -x+'px' : -self.limit + self.margin+'px'
      }
    }[event.target.nodeName.toLowerCase()])()
  }
  
  active(index) {
    // set active page and move to center
    $$('pages data list page')[index-1].className = 'active'
    let center = (parseInt(this.count / 2) + (this.count % 2)) * (this.width + this.margin)
    let current = index * (this.width + this.margin)
    let x = -parseInt(this.list.style.left) + (current - center)
    if(current > center) {
      this.list.style.left = (x <= this.limit) ? -x+'px' : -this.limit + this.margin+'px'
    }
    if(current < center) {
      this.list.style.left = (x > this.margin) ? -x+'px' : this.margin+'px'
    }
  }
}