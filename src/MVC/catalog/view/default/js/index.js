"use strict"

let LEGACY = !CSS.supports("container: name")

class Index {
  constructor() {
    $$.ready( () => {
      $$.css([
        '/default/css/1200/common.css',
        '/default/css/1200/header.css',
        '/default/css/1200/top.css',
        '/default/css/1200/menu.css',
        '/default/css/1200/page.css',
        '/default/css/1200/nav.css',
        '/default/css/1200/footer.css',
        '/default/css/1200/social.css',
        '/default/css/1200/index.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
        }
      )
    })
  }
}

let index = new Index()

