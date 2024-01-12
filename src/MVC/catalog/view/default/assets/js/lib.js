/*
Created: 2023.11.20
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function isDict(aData) {
    return (aData !== null) && (typeof aData === 'object')
}

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

class TFormChangeTracker {
    constructor(aFormId, aOptions = {}) {
        const defOption = {
            changed: 'vChanged',
            readonly: 'vReadonly'
        }
        this.options = { ...defOption, ...aOptions }

        this.initialValues = {}
        this.form = document.getElementById(aFormId)
        this.init()
    }

    getAttr(aElement, aName = 'name') {
        //return aElement[aName]
        return aElement.name || aElement.id
    }

    filter(aElement) {
        return (['text', 'number', 'hidden', 'checkbox'].includes(aElement.type) || ['SELECT', 'TEXTAREA'].includes(aElement.tagName)) && this.getAttr(aElement)
    }

    getInputs() {
        let Res = []
        Array.from(this.form.elements).forEach((element) => {
            if (this.filter(element)) {
                Res.push(element)
            }
        })
        return Res
    }

    init() {
        for (const x of this.getInputs()) {
            this.initialValues[this.getAttr(x)] = this.getValue(x)
        }

        this.form.addEventListener('input', (event) => {
            const element = event.target
            if (this.filter(element)) {
                const initialValue = this.initialValues[this.getAttr(element)]
                const currentValue = this.getValue(element)

                if (currentValue !== initialValue) {
                    element.classList.add(this.options.changed)
                    element.title = initialValue
                } else {
                    element.classList.remove(this.options.changed)
                    element.title = ''
                }
            }
        })
    }

    getChanges() {
        let Res = {}
        for (const x of this.getInputs()) {
            const value = this.getValue(x)
            if (this.initialValues[this.getAttr(x)] != value) {
                Res[this.getAttr(x)] = value
            }
        }
        return Res
    }

    undoChanges() {
        for (const x of this.getInputs()) {
            this.setValue(x, this.initialValues[this.getAttr(x)])
            x.classList.remove(this.options.changed)
        }
    }

    getValue(aElement) {
        if (aElement.type == 'checkbox') {
            return aElement.checked
        } else if (aElement.tagName == 'SELECT') {
            return aElement.options[aElement.selectedIndex].value
        } else {
            return aElement.value
        }
    }

    setValue(aElement, aValue) {
        if (aElement.type == 'checkbox') {
            aElement.checked = aValue
        } else if (aElement.tagName == 'SELECT') {
            aElement.options[aElement.selectedIndex].value = aValue
        } else {
            aElement.value = aValue
        }
    }

    setReadonly(aVal) {
        if (aVal) {
            this.form.classList.add(this.options.readonly)
        }else{
            this.form.classList.remove(this.options.readonly)
        }
    }

    submit(aTarget = null) {
        let newData = document.createElement('input')
        newData.type = 'hidden'
        newData.name = 'changes'
        newData.value = JSON.stringify(this.getChanges())
        this.form.appendChild(newData);
        if (aTarget) {
            newData = document.createElement('input')
            newData.type = 'hidden'
            newData.name = aTarget.name
            newData.value = aTarget.value
            this.form.appendChild(newData);
        }
        this.form.submit()
    }
}

function format(aPattern, aValues) {
    return aPattern.replace(/\{(\w+)\}/g, (match, key) => aValues[key] || match)
}

/*
let Redirect = new TRedirect('/admin/?route=product&product_id={id}')
Redirect.To({'id': 12})
*/
class TRedirect {
    constructor(aPattern) {
        this.pattern = aPattern
    }

    To(aValues) {
        const url = format(this.pattern, aValues)
        window.location.href = url
    }
}

function fetchGet(aUrl) {
    const requestOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'text/html'
      }
    }

    const Res = fetch(aUrl, requestOptions)
        .then(aResponse => {
            if (!aResponse.ok) {
                throw new Error(`HTTP error. Status: ${aResponse.status}`)
            }
            return aResponse
        })
        .then(aResponseData => {
            return aResponseData
        })
        .catch(aErr => {
            console.error('Err:', aErr)
        })
    return Res
}


function fetchPostJson(aUrl, aData = {}) {
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
            //throw error
        })
    return Res
}

function loadInto(aIdName, aUrl, aData = null) {
    function setElement(data) {
            console.log('x1', aIdName, aUrl, aData, data)
            //const element = document.getElementById(aIdName)
            //element.innerHTML = data
    }

    if (isDict(aData)) {
        fetchPostJson(aUrl, aData)
            .then(data => {
                setElement(data)
            })
    } else {
        fetchGet(aUrl)
            .then(data => {
                setElement(data)
            })
    }
}

function assert(aCond, aMsg = 'Error') {
    if (!aCond) {
        throw new Error(aMsg || ' assertion failed')
    }
}

function changeImage(aImg, aId, aHref = false) {
    const element = document.getElementById(aId)
    element.src = aImg.src
    if (aHref) {
        element.parentNode.href = aImg.src
    }
}
