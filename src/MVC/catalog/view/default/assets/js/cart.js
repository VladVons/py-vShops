/*
Created: 2023.11.07
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


class TShoppingCart {
    constructor() {
        this.Items = {}
        this.storageId = this.constructor.name
        this.loadFromStorage()
    }

    clear() {
        this.Items = {}
        this.saveToStorage()
    }

    getCount() {
        return Object.keys(this.Items).length;
    }

    getDbl() {
        let data = []
        for (const [key, val] of Object.entries(this.Items)) {
            data.push([parseInt(val.id), val.name, parseFloat(val.qty), parseFloat(val.price), val.href, val.img])
        }

        return {
            'head': ['id', 'name', 'qty', 'price', 'href', 'img'],
            'data': data,
            'tag': this.storageId
        }
        return JSON.stringify(this.Items)
    }

    getTotal() {
        let Qty = 0
        let Sum = 0
        for (const [key, val] of Object.entries(this.Items)) {
            Qty += val.qty
            Sum += val.qty * val.price
        }
        return {'qty': Qty, 'sum': Sum}
    }

    saveToStorage() {
        localStorage.setItem(this.storageId, JSON.stringify(this.Items))
    }

    loadFromStorage() {
        const Data = localStorage.getItem(this.storageId)
        if (Data) {
            this.Items = JSON.parse(Data)
        }
    }

    itemAdd(aData) {
        if (this.itemExists(aData.id)) {
            aData.qty += this.Items[aData.id].qty
        }
        this.itemSet(aData)
    }

    itemDel(aId) {
        delete this.Items[aId]
        this.saveToStorage()
    }

    itemExists(aId) {
        return aId in this.Items
    }

    itemSet(aData) {
        this.Items[aData.id] = aData
        this.saveToStorage()
    }

    itemSetQty(aId, aQty) {
        if (aQty >= 0) {
            this.Items[aId].qty = aQty
            this.saveToStorage()
        } else {
            //this.itemDel(aKey)
        }
    }
}

ShoppingCart = new TShoppingCart()
//ShoppingCart.clear()


function buildCart() {
    let Arr = []
    for (const [key, val] of Object.entries(ShoppingCart.Items)) {
        const Data = `
        <div class="row align-items-center mb-2">
            <div class="col-md-3">
                <a href="${val.href}"><img class="img-fluid rounded-3" style="width: 80px" src="${val.img}"></a>
            </div>
            <div class="col-md-3">
                <p>${val.name}</p>
            </div>
            <div class="col-md-1">
                <input type='number' class='form-control vInputQty viItemQty' data-id='${val.id}' value='${val.qty}' min='0'>
            </div>
            <div class="col-md-2">
                ${val.price} грн
            </div>
            <div class="col-md-2 fw-bold">
                ${val.qty * val.price} грн
            </div>
            <div class="col-md-1">
                <button class="btn btn-danger viItemDel" data-id="${val.id}" title="delete">X</button>
            </div>
        </div>
        `
        Arr.push(Data)
    }

    const Total = ShoppingCart.getTotal()

    document.querySelector('.viCartItems').innerHTML = Arr.join('')
    document.querySelector('.viTotalSum').innerHTML = Total.sum
    document.getElementById('viCount_cart').innerHTML = (Total.qty == 0 ? null : Total.qty)
}

const defaultBtns = document.querySelectorAll(".viAddToCart")
defaultBtns.forEach(function (btn) {
    btn.addEventListener('click', function (event) {
        event.preventDefault()
        let data = btn.getAttribute('data-product')
        data = JSON.parse(data)

        const Missed = hasAllKeys(data, ['id', 'name', 'img', 'price', 'href'])
        const Msg = `missed required keys ${Missed}`
        console.assert(Missed.length == 0, Msg)

        if (ShoppingCart.itemExists(data.id)) {
            showTooltip(gData.getValue('/lang/already_in_cart'))
        }else{
            showTooltip(gData.getValue('/lang/added_to_cart'))
            ShoppingCart.itemAdd(data)
            buildCart()
        }
    })
})

const CartItems = document.querySelector('.viCartItems')
CartItems.addEventListener('click', function (event) {
    if (event.target.classList.contains('viItemDel')) {
    //if (event.target.id == 'viDelItem') {
    //if (event.target.getAttribute('data-type') == 'viDelItem') {
        const id = event.target.getAttribute('data-id')
        ShoppingCart.itemDel(id)
        buildCart()
    }
})

CartItems.addEventListener('change', function (event) {
    if (event.target.classList.contains('viItemQty')) {
        const id = event.target.getAttribute('data-id')
        const qty = parseInt(event.target.value)
        ShoppingCart.itemSetQty(id, qty)
        buildCart()
    }
})

const clearAll = document.querySelector('.viClearAll')
clearAll.addEventListener('click', function (event) {
    ShoppingCart.clear()
    buildCart()
})


buildCart()
