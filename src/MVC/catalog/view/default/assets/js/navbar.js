/*
Created: 2023.11.30
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function navbarCategoryClick() {
    function Recurs(aData, aId) {
        let Res = []
        for (let x of aData[aId]) {
            if (x.id in aData) {
                Res.push('<li class="nav-item dropdown">')
                Res.push(`<a class="dropdown-item dropdown-toggle" href="${x.href}" role="button" data-bs-toggle="dropdown">${x.title} (${x.products})</a>`)
                Res.push('<ul class="dropdown-menu">')
                let ResR = Recurs(aData, x.id)
                Res = Res.concat(ResR)
                Res.push('</ul>')
                Res.push('</li>')
            }else{
                Res.push(`<li><a class="dropdown-item" href="${x.href}">${x.title} (${x.products})</a></li>`)
            }
        }
        return Res
    }

    function displayResults(aData) {
        let Data = Recurs(aData, 0)
        let navbarItems = document.getElementById('viMainNavbarItems')
        navbarItems.innerHTML = Data.join('\n')
        navbarSubmenu({"selector": "viMainNavbar"})
    }

    var url = gData.getValue('/href/category_ajax')
    postJson(url, {'method': 'ajax'})
        .then(data => {
            displayResults(data)
        })
}

function navbarSubmenu(aOptions) {
    const defaultOption = {
        selector: "viMainNavbar"
    }
    const Options = { ...defaultOption, ...aOptions }
    var dropdowns = document.getElementById(Options.selector).getElementsByClassName("dropdown")

    Array.prototype.forEach.call(dropdowns, (item) => {
        item.addEventListener("mouseover", function () {
            this.classList.add("show")
            const element = this.querySelector(".dropdown-menu")
            element.classList.add("show")
        })

        item.addEventListener("mouseout", function () {
            this.classList.remove("show")
            const element = this.querySelector(".dropdown-menu")
            element.classList.remove("show")
        })
    })
}

navbarSubmenu({"selector": "viMainNavbar"})
