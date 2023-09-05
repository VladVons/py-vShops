"use strict"

// User imports
import {conf} from './conf.js'

class Search {
  constructor() {
    $$( () => {
      $$('input.search').on('keypress', (event) => {
        if(event.keyCode == 13 && event.target.value.length >= 3) {
          document.location.href = conf.url.search + encodeURI(event.target.value)
        }
      })
      $$('button.search').on('click', (event) => { 
        let input = $$('input.search')[0]
        if(input.value.length >= 3) {
          document.location.href = conf.url.search + encodeURI(input.value)
        }
      })
    })
  }
}

new Search()

