"use strict"

let LEGACY = !CSS.supports("container: name")

class Item {
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
        '/default/css/1200/product.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
          
          //set listeners
          let tabs = $$('tabs tab')
          for(let i=0; i<tabs.length; i++) {
            tabs[i].addEventListener('click', self.setActive.bind(self))
          }
          
          //set thumbs
          let thumbs = $$('thumbs thumb')
          for(let i=0; i<thumbs.length; i++) {
            thumbs[i].addEventListener('click', self.setImage.bind(self))
          }
          
        }
      )
    })
  }
  
  setActive(event) {
    let tabs = $$('tabs panel tab')
    for(let i=0; i<tabs.length; i++) {
      if(tabs[i] == event.target) {
        event.target.classList.add('active')
        $$('tabs data label.'+event.target.id)[0].classList.remove('hide')
      }else{
        tabs[i].classList.remove('active')
        $$('tabs data label.'+tabs[i].id)[0].classList.add('hide')
      }
    }
  }
  
  setImage(event) {
    $$('zoom img')[0].src = event.target.style.backgroundImage.match(/url\(['"]?([^'"]+)['"]?\)/)[1]
  }
  
}

window.item = new Item()
