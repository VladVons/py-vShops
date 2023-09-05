"use strict"

// jMagic imports
await $$.import('plugins.scss')

// User imports
import {conf} from '../../conf.js'
import('../../common.js')

const
  PATH = 'information/contact',
  GPS = [49.55133, 25.5980, 19]

class Contact {

  #map = null
  #google = null
  
  constructor() {
    let self = this

    $$(async () => {
      //load css rules
      
      let rules = await SCSS.load([
        `${$$.conf.path.css}/common.css`,
        `${$$.conf.path.css}/desktop/contact.css`,
        `${$$.conf.path.leaflet}/css/leaflet.css`])
      $$.css(SCSS.dump(rules))
      
      //load localization
      this.lang = await $$.post(conf.url.local, { 
        headers : { 'Content-type': 'application/json' },
        body    : JSON.stringify({ path: PATH, lang: 'ua', key: 'js' }),
      })
      
      //unmask page
      $$('body').css({opacity: 1})
      
      //init map
      this.map(...GPS)
      
      $$('title.fl')
        .on('click', this.map.bind(this))
      $$('title.fr')
        .on('click', this.google.bind(this))
      
    })
  }
  
  toggle() {
    let node = $$('map')[0]
    for(let child of node.childNodes) {
      child.classList.toggle('hide')
    }
    return node
  }
  
  map(x, y, z) {
    let node = this.toggle()
    if(this.#map) return false
    this.#map = L.map(node)
    this.#map.setView([x, y], z)
    let tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(this.#map)
    
    L.marker([x, y]).addTo(this.#map)
      .bindPopup(`<marker><name>${this.lang.map_name}</name><addr>${this.lang.map_addr}</addr></marker>`)
      .openPopup();
  }
  
  google() {
    let node = this.toggle()
    if(this.#google) return false
    let iframe = $$('<iframe></iframe>')
      .attr({width: '100%', height: '100%', allowfullscreen: '', loading: 'lazy', referrerpolicy: 'no-referrer-when-downgrade',
        style: "border:0; border-radius: 8px;",
        src: 'https://www.google.com/maps/embed?'+'pb=!4v1682438748439!6m8!1m7!1s3bMuMeLz-V7u8KEqJcWN7w!2m2!1d49.55124248764106'+'!2d25.59806692213795!3f301.0502188094272!4f2.324733174187017!5f0.7820865974627469'})[0]
    
    node.appendChild(iframe)
  }
  
}

new Contact
