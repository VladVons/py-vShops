// Telegram Extension for jMagic
"use strict"

const 
  TG_ID     = `-1001976537532`,
  TG_TOKEN  = `5671254016:AAEFjWObM1uJSqzDXRTbUT4379ieHIU6whc`,
  TG_URL    = `https://api.telegram.org/bot${TG_TOKEN}`


export class Telegram {
  
  constructor() {
    this.token = TG_TOKEN
    this.url = TG_URL
    this.id = TG_ID
    this.headers = {'Content-Type': 'application/json'}
  }
  
  send(text, options = {command: 'sendMessage'}) {
    return new Promise((resolve,reject) => {
      $$.post(`${this.url}/${options.command}`, {
        headers : this.headers,
        body    : JSON.stringify({
          chat_id: this.id, 
          parse_mode: 'HTML',
          text: text, 
        })
      })
      .then(json => {
        resolve(json.result)
      })
      .catch(error => {
        console.log(error)
        $$.tip('Помилка Телеграм!')
        reject(error)
      })
    })
  }
}