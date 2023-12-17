/*
Created: 2023.11.20
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


class TDict {
    constructor() {
        this.data = {}
    }

    getValue(aPath) {
        const keys = aPath.split('/').filter(key => key !== '')
        let obj = this.data
        for (const key of keys) {
            obj = obj[key]
            if (obj == undefined) {
                return obj
            }
        }
        return obj
    }

    setValue(aPath, aVal) {
        const keys = aPath.split('/').filter(key => key !== '')
        let obj = this.data
        for (const key of keys.slice(0, -1)) {
            if (!obj.hasOwnProperty(key)) {
                obj[key] = {}
            }
            obj = obj[key]
        }

        const keyLast = keys[keys.length - 1]
        obj[keyLast] = aVal
    }

    updValue(aPath, aVal) {
        const obj = this.getValue(aPath)
        if (obj != undefined && obj.constructor == Object && aVal.constructor == Object){
            aVal = { ...obj, ...aVal}
        }
        this.setValue(aPath, aVal)
    }
}

/*
let Redirect = new TRedirect('/tenant/?route=product&product_id={id}')
Redirect.To({'id': 12})
*/
class TRedirect {
    constructor(aPattern) {
        this.pattern = aPattern
    }

    To(aValues) {
        const url = this.pattern.replace(/\{(\w+)\}/g, (match, key) => aValues[key] || match)
        window.location.href = url
    }
}

function postJson(aUrl, aData = {}) {
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
      },
      body: JSON.stringify(aData)
    }

    const Res = fetch(aUrl, requestOptions)
        .then(aResponse => {
            if (!aResponse.ok) {
                throw new Error(`HTTP error. Status: ${aResponse.status}`)
            }
            return aResponse.json()
        })
        .then(aResponseData => {
            return aResponseData
        })
        .catch(aErr => {
            console.error('Err:', aErr)
        })
    return Res
    /*
    return fetch(aUrl, requestOptions)
        .then(response => response.json())
        .then(responseData => {
            console.log('Success:', responseData);
            return responseData
        })
        .catch(error => {
            console.error('Error:', error);
            throw error
        })
    */
}

function assert(aCond, aMsg = 'Error') {
  if (!aCond) {
    throw new Error(aMsg || " assertion failed")
  }
}

function changeImage(aImg, aId, aHref = false) {
    const element = document.getElementById(aId)
    element.src = aImg.src
    if (aHref) {
        element.parentNode.href = aImg.src
    }
}


function showTooltip(aMsg, aId = null) {
    const tooltip = document.createElement("div")
    tooltip.classList.add("tooltip")
    tooltip.textContent = aMsg
    if (aId) {
        const element = document.getElementById(aId)
        const rect = element.getBoundingClientRect()

        /*
        // ToDo. extra width
        tooltip.style.left = rect.left + 'px'
        tooltip.style.top = (rect.top + rect.height) + 'px'
        tooltip.style.right = 0
        console.log(tooltip.style.width)
        */
    }

    document.body.appendChild(tooltip)

    // apply the initial styles
    tooltip.offsetWidth

    tooltip.classList.add("active")

    setTimeout(function () {
        tooltip.classList.remove("active")
        setTimeout(function () {
            document.body.removeChild(tooltip)
        }, 300)
    }, 2000)
}
