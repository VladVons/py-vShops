/*
Created: 2023.12.01
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details

as function namespace
*/


function searchNavbar() {
    const autocompleteActive = 'autocomplete-active'
    let curFocus = 0
    let timeout = null

    const elSearchInput = document.getElementById('viSearchInput')
    assert(elSearchInput, 'viSearchInput')
    const elSearchSuggest = document.getElementById('viSearchSuggest')
    assert(elSearchSuggest)

    document.addEventListener('click', function(event) {
        if (!elSearchSuggest.contains(event.target)) {
          elSearchSuggest.innerHTML = ''
          //elSearchInput.value = ''
        }
    })

    elSearchInput.addEventListener('keydown', function(aEvent) {
        let x = elSearchSuggest.getElementsByTagName('div')
        if (x.length == 0)
            return

        if (aEvent.key == 'ArrowDown') {
            curFocus++
            setActive(x)
        } else if (aEvent.key == 'ArrowUp') {
            curFocus--
            setActive(x)
        } else if (aEvent.key == 'Enter') {
            aEvent.preventDefault()
            if (curFocus >= 0) {
                x[curFocus].click()
            }
        } else if (aEvent.key == 'Escape') {
            elSearchSuggest.innerHTML = ''
        } else {
            curFocus = -1
        }
    })

    elSearchInput.addEventListener('input', function(aEvent) {
        clearTimeout(timeout)
        timeout = setTimeout(() => {
            const value = this.value.trim()
            if (value.length > 0) {
                const url = gData.getValue('/href/search_ajax')
                new TSend().execA(url, {'method': 'ajax', 'q': value})
                    .then(data => {
                        displayResult(aEvent, data)
                    })
            } else {
                elSearchSuggest.innerHTML = ''
            }
        }, 500)
    })

    function displayResult(aEvent, aResults) {
        elSearchSuggest.innerHTML = ''

        if (aResults && aResults.length > 0) {
            const keys = aEvent.target.value.split(' ').filter(key => key !== '')
            //const pattern = new RegExp(`\\b(${keys.join('|')})\\b`, 'gi')
            const pattern = new RegExp(`(${keys.join('|')})`, 'gi')

            aResults.forEach(function(aResult) {
                const elDiv = document.createElement('div')
                elDiv.innerHTML = aResult.replace(pattern, '<b>$1</b>') + `<input type='hidden' value='${aResult}'>`
                elDiv.addEventListener("click", function(e) {
                    const value = this.getElementsByTagName("input")[0].value
                    aEvent.target.value = value
                    elSearchSuggest.innerHTML = ''
                    window.location.href = '?route=product0/search&q=' + encodeURIComponent(value)
                })
                elSearchSuggest.appendChild(elDiv)
            })
        }
    }

    function setActive(x) {
        delActive(x)

        if (curFocus >= x.length)
            curFocus = 0

        if (curFocus < 0)
            curFocus = (x.length - 1)

        x[curFocus].classList.add(autocompleteActive)
    }

    function delActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove(autocompleteActive)
        }
    }
}

searchNavbar()
