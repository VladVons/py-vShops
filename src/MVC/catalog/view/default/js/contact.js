"use strict"

let LEGACY = !CSS.supports("container: name")

class Contact {
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
        '/default/css/1200/contact.css'
        ],
        () => {
          $$('body').css({display: 'initial'})
          
          //init map
          self.mapInit(49.55134, 25.5980, 18)
        }
      )
    })
  }
  
  mapInit(x, y, z) {
    let map = L.map('map').setView([x, y], z)
    let tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map)
    
    L.marker([x, y]).addTo(map)
      .bindPopup("<popup><name>Комп'ютерний магазин «ОСТЕР»</name><addr>м.Тернопіль, вул. Руська 41/3</addr></popup>")
      .openPopup();
  }
  
  googleInit(a) {
    a.parentNode.insertBefore($$("<google><close title='закрити вікно'>Комп'ютерний магазин «ОСТЕР»</close></google>")[0], a)
    $$('google').css({top: '100px', left: '100px', width: 'calc(100% - 200px)', height: 'calc(100% - 200px)'})
    let iframe = $$('<iframe></iframe>')
      .attr({width: '100%', height: '100%', allowfullscreen: '', loading: 'lazy', referrerpolicy: 'no-referrer-when-downgrade',
        src: 'https://www.google.com/maps/embed?'+'pb=!4v1682438748439!6m8!1m7!1s3bMuMeLz-V7u8KEqJcWN7w!2m2!1d49.55124248764106'+'!2d25.59806692213795!3f301.0502188094272!4f2.324733174187017!5f0.7820865974627469'})
    $$('google')[0].appendChild(iframe[0])
    $$('google close')[0].addEventListener('click', (event) => {
      let google = $$('google')[0]
      google.parentNode.removeChild(google)
    })
  }
  
  message() {
    alert('Відправка форми на сервер')
    return false
  }
}

window.contact = new Contact()
