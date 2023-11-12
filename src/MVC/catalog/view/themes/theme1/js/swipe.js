"use strict"

export class Swipe {
  constructor(element) {
    this.dx = 30 //delta for x
    this.dy = 30 //delta for y
    this.node = $$(element)[0]
    this.x = null
    this.y = null
    this.node.addEventListener('touchstart', event => {
      this.x = event.touches[0].clientX;
      this.y = event.touches[0].clientY;
    })
    this.node.addEventListener('touchmove', event => {
      let x = event.touches[0].clientX;
      let y = event.touches[0].clientY;
      if((this.x - x) > this.dx) {
        this.node.style.left = '-' + this.node.scrollWidth + 'px'
      }
    })
    //document
    $$('body')
      .on('touchstart', event => {
        this.x = event.touches[0].clientX;
        this.y = event.touches[0].clientY;
      })
      .on('touchmove', event => {
        let x = event.touches[0].clientX;
        let y = event.touches[0].clientY;
        if((x - this.x) > this.dx && this.x < this.dx*2) {
          this.node.style.left = 0
        }
    })
  }
}
