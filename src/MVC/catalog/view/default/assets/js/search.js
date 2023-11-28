/*
Created: 2023.11.25
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


var searchInput = document.getElementById('viSearchInput')
var searchSuggest = document.getElementById('viSearchSuggest')

function postJson(aUrl, aData = {}) {
    const requestOptions = {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
      },
      body: JSON.stringify(aData)
    }

    let Res = fetch(aUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`)
            }
            return response.json()
        })
        .catch(error => {
            console.error('Error:', error)
        })
    return Res
}

searchInput.addEventListener('input', function(aEvent) {
    var searchTerm = this.value.trim()
    if (searchTerm.length > 0) {
        // encodeURIComponent(searchTerm)
        var url = gData.getValue('/href/search_ajax')
        postJson(url, {'method': 'ajax', 'q': searchTerm})
            .then(data => {
                displayResults(aEvent, data)
            })
    }else{
        searchSuggest.innerHTML = ''
    }
})

function displayResults(aEvent, aResults) {
    searchSuggest.innerHTML = ''

    if (aResults && aResults.length > 0) {
        aResults.forEach(function(aResult) {
            var option = document.createElement('option')
            option.value = aResult
            searchSuggest.appendChild(option)
        })

        var selectedValue = aEvent.target.value
        if (aResults.includes(selectedValue)) {
            window.location.href = gData.getValue('href/search') + encodeURIComponent(selectedValue)
        }
    } else {
        searchSuggest.innerHTML = ''
    }
}
