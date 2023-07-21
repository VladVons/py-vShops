"use strict"

const searchURL = '?route=product/search&search='

class Search {
  constructor() {
    $$( () => {
      $$('input.search').on('keypress', (event) => {
        if(event.keyCode == 13 && event.target.value.length >= 3) {
          document.location.href = searchURL + encodeURI(event.target.value)
        }
      })
      $$('button.search').on('click', (event) => { 
        let input = $$('input.search')[0]
        if(input.value.length >= 3) {
          document.location.href = searchURL + encodeURI(input.value)
        }
      })
    })
  }
}

new Search()

