"use strict"

const searchURL = '?route=product/search&search='

class Search {
  constructor() {
    $$.ready( () => {
      $$('input.search')[0].addEventListener('keypress', (event) => {
        if(event.keyCode == 13 && event.target.value.length >= 3) {
          document.location.href = searchURL + encodeURI(event.target.value)
        }
      })
      $$('button.search')[0].addEventListener('click', (event) => { 
        let input = $$('input.search')[0]
        if(input.value.length >= 3) {
          document.location.href = searchURL + encodeURI(input.value)
        }
      })
    })
  }
}

let search = new Search()

