/*
Created: 2023.12.01
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details

as function namespace
*/


function searchNavbar() {
    let timeout = null
    const elSearchInput = document.getElementById('viSearchInput')
    const elSearchSuggest = document.getElementById('viSearchSuggest')

    elSearchInput.addEventListener('input', function(aEvent) {
        const value = this.value.trim()
        if (value.length > 0) {
            clearTimeout(timeout)
            timeout = setTimeout(() => {
                const url = gData.getValue('/href/search_ajax')
                postJson(url, {'method': 'ajax', 'q': value})
                    .then(data => {
                        displayResult(aEvent, data)
                    })
            }, 500)
        } else {
            elSearchSuggest.innerHTML = ''
        }
    })

    function displayResult(aEvent, aResults) {
        elSearchSuggest.innerHTML = ''

        if (aResults && aResults.length > 0) {
            //const keys = aEvent.target.value.split(' ').filter(key => key !== '')
            //const pattern = new RegExp(`\\b(${keys.join('|')})\\b`, 'gi')

            aResults.forEach(function(aResult) {
                let option = document.createElement('option')
                option.value = aResult
                //option.value = aResult.replace(pattern, '<b>$1</b>')
                elSearchSuggest.appendChild(option)
            })

            const selectedValue = aEvent.target.value
            if (aResults.includes(selectedValue)) {
                window.location.href = '?route=product0/search&q=' + encodeURIComponent(selectedValue)
            }
        }
    }
}

searchNavbar()
