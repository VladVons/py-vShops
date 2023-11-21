/*
Created: 2023.11.07
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


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
            Qty += val.Qty
            Sum += val.Qty * val.Price
        }
        return {'Qty': Qty, 'Sum': Sum}
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

    itemAdd(aKey, aName, aPrice, aImg, aQty) {
        if (this.itemExists(aKey)) {
            aQty += this.Items[aKey].Qty
        }
        this.itemSet(aKey, aName, aPrice, aImg, aQty)
    }

    itemDel(aKey) {
      delete this.Items[aKey]
      this.saveToStorage()
    }

    itemExists(aKey) {
        return aKey in this.Items
    }

    itemSet(aKey, aName, aPrice, aImg, aQty) {
        this.Items[aKey] = {'Name': aName, 'Price': aPrice, 'Img': aImg, 'Qty': aQty}
        this.saveToStorage()
    }

    itemSetQty(aKey, aQty) {
        if (aQty >= 0) {
            this.Items[aKey].Qty = aQty
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
                <a href="#"><img class="img-fluid rounded-3" style="width: 80px" src="${val.Img}" alt="image xyz"></a>
            </div>
            <div class="col-md-3">
                <p>${val.Name}</p>
            </div>
            <div class="col-md-1">
                <input type='number' class='form-control vInputQty viItemQty' data-name='${val.Name}' value='${val.Qty}'>
            </div>
            <div class="col-md-2">
                ${val.Price} грн
            </div>
            <div class="col-md-2 fw-bold">
                ${val.Qty * val.Price} грн
            </div>
            <div class="col-md-1">
            <button class="btn btn-danger viItemDel" data-name="${val.Name}" title="delete">X</button>
        </div>
        </div>
        `
        Arr.push(Data)
    }

    var Total = ShoppingCart.getTotal()

    document.querySelector('.viCartItems').innerHTML = Arr.join('')
    document.querySelector('.viTotalSum').innerHTML = Total.Sum
    document.querySelector('.viTotalCount').innerHTML = Total.Qty
}

const defaultBtns = document.querySelectorAll(".viAddToCart");
defaultBtns.forEach(function (btn) {
    btn.addEventListener('click', function (event) {
        event.preventDefault()
        const name = btn.getAttribute('data-name')
        const price = parseFloat(btn.getAttribute('data-price'))
        const img = btn.getAttribute('data-img')
        if (ShoppingCart.itemExists(name)) {
            showTooltip(gData.lang.already_in_cart)
        }else{
            showTooltip(gData.lang.added_to_cart)
            ShoppingCart.itemAdd(name, name, price, img, 1)
            buildCart()
        }
    })
})

const CartItems = document.querySelector('.viCartItems');
CartItems.addEventListener('click', function (event) {
    if (event.target.classList.contains('viItemDel')) {
    //if (event.target.id == 'viDelItem') {
    //if (event.target.getAttribute('data-type') == 'viDelItem') {
        const name = event.target.getAttribute('data-name');
        ShoppingCart.itemDel(name)
        buildCart()
    }
})

CartItems.addEventListener('change', function (event) {
    if (event.target.classList.contains('viItemQty')) {
        const name = event.target.getAttribute('data-name');
        const qty = parseInt(event.target.value)
        ShoppingCart.itemSetQty(name, qty)
        buildCart()
    }
})

const clearAll = document.querySelector('.viClearAll');
clearAll.addEventListener('click', function (event) {
    ShoppingCart.clear();
    buildCart();
})


buildCart()
