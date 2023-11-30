/*
Created: 2023.11.25
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


var searchInput = document.getElementById('viSearchInput')
var searchSuggest = document.getElementById('viSearchSuggest')

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
        const keys = aEvent.target.value.split(' ').filter(key => key !== '')
        const pattern = new RegExp(`\\b(${keys.join('|')})\\b`, 'gi')

        aResults.forEach(function(aResult) {
            var option = document.createElement('option')
            option.value = aResult
            //option.value = aResult.replace(pattern, '<b>$1</b>')
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
