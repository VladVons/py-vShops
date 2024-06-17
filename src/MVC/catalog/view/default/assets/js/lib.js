/*
Created: 2023.11.20
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function isDict(aData) {
    return (aData !== null) && (typeof aData === 'object')
}

class TLocalStorage {
    constructor(aStorageId) {
        this.storageId = aStorageId
        this.items = null
        this.load()
    }

    save() {
        if (this.items) {
            localStorage.setItem(this.storageId, JSON.stringify(this.items))
        }
    }

    load() {
        const data = localStorage.getItem(this.storageId)
        if (data) {
            this.items = JSON.parse(data)
        }
    }

    remove() {
        this.items = null
        localStorage.removeItem(this.storageId)
    }

    addItemToList(aItem) {
        this.items.push(aItem)
    }

    addItemToListUniq(aItem) {
        if (this.items == null) {
            this.items = [aItem]
        } else if (!this.items.includes(aItem)) {
            this.addItemToList(aItem)
        }
    }

    addItemToListCycle(aItem, aMax = 5) {
        this.addItemToListUniq(aItem)
        if (this.items.length > aMax) {
            this.items.shift()
        }
    }
}

class TDict {
    constructor(aData = {}) {
        this.data = aData
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

    merge(aDict) {
        this.data = { ...this.data, ...aDict }
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
        const inputs = this.getInputs()
        //console.log('-x2', this.form, inputs)
        for (const x of inputs) {
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
        const inputs = this.getInputs()
        //console.log('-x2', inputs)
        for (const x of inputs) {
            const value = this.getValue(x)
            const prev = this.initialValues[this.getAttr(x)]
            if (prev != value) {
                Res[this.getAttr(x)] = [prev, value]
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

    saveToStorage() {
        let Data = {}
        for (const x of this.getInputs()) {
            Data[this.getAttr(x)] = this.getValue(x)
        }
        localStorage.setItem(this.form.id, JSON.stringify(Data))
    }

    loadFromStorage() {
        let Data = localStorage.getItem(this.form.id)
        if (Data) {
            Data = JSON.parse(Data)
            for (const x of this.getInputs()) {
                let Key = this.getAttr(x)
                this.setValue(x, Data[Key])
            }
        }
    }

    checkEmpty(aElements) {
        let Res = []
        for (const x of this.getInputs()) {
            const Key = this.getAttr(x)
            if ((aElements.indexOf(Key) !== -1) && (! this.getValue(x))) {
                Res.push(x)
            }
        }
        return Res
    }

    submit(aHiddens = [], aAsRequest = false) {
        let newData = document.createElement('input')
        newData.type = 'hidden'
        newData.name = 'changes'
        newData.value = JSON.stringify(this.getChanges())
        this.form.appendChild(newData)

        newData = document.createElement('input')
        newData.type = 'hidden'
        newData.name = 'formId'
        newData.value = this.form.id
        this.form.appendChild(newData)

        for (const x of aHiddens) {
            newData = document.createElement('input')
            newData.type = 'hidden'
            newData.name = x.name
            newData.value = x.value
            this.form.appendChild(newData)
        }

        if (aAsRequest) {
            const formData = new FormData(this.form)
            return new TSend().exec(this.form.action, formData)
        } else {
            this.form.submit()
        }
    }
}

class TSend {
    param(aUrl, aData) {
        let method = 'GET'
        let contentType = 'text/html'
        let type = 'text'

        if (aData != null) {
            method = 'POST'
            if (aData instanceof FormData) {
                //contentType = 'multipart/form-data'
                contentType = null // new FormData() handles itself
                type = 'form-data'
            } else if (isDict(aData)) {
                contentType = 'application/json'
                type = 'json'
                aData = JSON.stringify(aData)
            }
        }
        return {'url': aUrl, 'data': aData, 'method':  method, 'contentType': contentType, 'type': type}
    }

    exec(aUrl, aData = null) {
        const param = this.param(aUrl, aData)
        const request = new XMLHttpRequest()
        request.open(param.method, param.url, false)
        if (param.contentType) {
            request.setRequestHeader('Content-type', param.contentType)
        }
        request.send(param.data)
        if (request.status == 200) {
            if (param.type == 'json') {
                return JSON.parse(request.responseText)
            } else {
                return request.responseText
            }
        } else {
            console.error('Err', request.status)
        }
    }

    execA(aUrl, aData = null) {
        const param = this.param(aUrl, aData)
        const requestOptions = {
            method: param.method,
            headers: {
                'Content-Type': param.contentType,
          },
          body: param.data
        }

        const Res = fetch(aUrl, requestOptions)
            .then(aResponse => {
                if (!aResponse.ok) {
                    throw new Error(`HTTP error. Status: ${aResponse.status}`)
                }

                if (param.contentType == 'application/json') {
                    return aResponse.json()
                } else {
                    return aResponse.text()
                }
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
}

function sendInto(aIdName, aUrl, aData = null) {
    const element = document.getElementById(aIdName)
    element.innerHTML = new TSend().exec(aUrl, aData)
}

function sendMultiFile(aIdName, aUrl)
{
    const fileInput = document.getElementById(aIdName)
    if (fileInput.files.length > 0) {
        const formData = new FormData()
        for (let i = 0; i < fileInput.files.length; i++) {
            formData.append('files', fileInput.files[i])
        }
        new TSend().exec(aUrl, formData)

        //var xhr = new XMLHttpRequest()
        //xhr.open('POST', aUrl, true)
        //xhr.send(formData)
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

function IterNameValue(aElements) {
    let res = {}
    aElements.forEach(element => res[element.name] = element.value)
    return res
}

function dictMerge(aDict1, aDict2) {
    return { ...aDict1, ...aDict2 }
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-71xx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8)
        return v.toString(16);
    })
}

function hasAllKeys(aObj, aRequiredKeys) {
    const objKeys = new Set(Object.keys(aObj))
    const requiredKeys = new Set(aRequiredKeys)
    //return [...requiredKeys].every(key => objKeys.has(key))
    return [...requiredKeys].filter(key => !objKeys.has(key))
}

function isDesktopDevice() {
    return window.matchMedia("(min-width: 992px)").matches
}
