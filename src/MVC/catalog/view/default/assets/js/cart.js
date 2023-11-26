/*
Created: 2023.11.07
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function hasAllKeys(aObj, aRequiredKeys) {
    const objKeys = new Set(Object.keys(aObj));
    const requiredKeys = new Set(aRequiredKeys);
    //return [...requiredKeys].every(key => objKeys.has(key));
    return [...requiredKeys].filter(key => !objKeys.has(key));
}


class TShoppingCart {
    constructor() {
        this.Items = {}
        this.storageId = this.constructor.name;
        this.loadFromStorage()
    }

    clear() {
        this.Items = {}
        this.saveToStorage()
    }

    getTotal() {
        var Qty = 0
        var Sum = 0
        for (var [key, val] of Object.entries(this.Items)) {
            Qty += val.qty
            Sum += val.qty * val.price
        }
        return {'qty': Qty, 'sum': Sum}
    }

    saveToStorage() {
        localStorage.setItem(this.storageId, JSON.stringify(this.Items))
    }

    loadFromStorage() {
        let Data = localStorage.getItem(this.storageId)
        if (Data) {
            this.Items = JSON.parse(Data);
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
    var Arr = [];
    for (var [key, val] of Object.entries(ShoppingCart.Items)) {
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

    var Total = ShoppingCart.getTotal()

    document.querySelector('.viCartItems').innerHTML = Arr.join('')
    document.querySelector('.viTotalSum').innerHTML = Total.sum
    document.querySelector('.viTotalCount').innerHTML = Total.qty
}

const defaultBtns = document.querySelectorAll(".viAddToCart");
defaultBtns.forEach(function (btn) {
    btn.addEventListener('click', function (event) {
        event.preventDefault()
        var data = btn.getAttribute('data')
        data = JSON.parse(data);

        const Missed = hasAllKeys(data, ['id', 'name', 'img', 'price', 'href'])
        const Msg = `missed required keys ${Missed}`;
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

const CartItems = document.querySelector('.viCartItems');
CartItems.addEventListener('click', function (event) {
    if (event.target.classList.contains('viItemDel')) {
    //if (event.target.id == 'viDelItem') {
    //if (event.target.getAttribute('data-type') == 'viDelItem') {
        const id = event.target.getAttribute('data-id');
        ShoppingCart.itemDel(id)
        buildCart()
    }
})

CartItems.addEventListener('change', function (event) {
    if (event.target.classList.contains('viItemQty')) {
        const id = event.target.getAttribute('data-id');
        const qty = parseInt(event.target.value)
        ShoppingCart.itemSetQty(id, qty)
        buildCart()
    }
})

const clearAll = document.querySelector('.viClearAll');
clearAll.addEventListener('click', function (event) {
    ShoppingCart.clear();
    buildCart();
})


buildCart()
