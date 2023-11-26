/*
Created: 2023.11.25
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


var searchInput = document.getElementById('viSearchInput');
var searchSuggest = document.getElementById('viSearchSuggest');

searchInput.addEventListener('input', function(aEvent) {
    var searchTerm = this.value.trim();

    if (searchTerm.length > 1) {
        var url = 'assets/cgi/search.py?q=' + encodeURIComponent(searchTerm);

    // fetch API
    fetch(url)
        .then(response => response.json())
        .then(data => displayResults(aEvent, data))
        .catch(error => console.error('Error fetching data:', error));
    } else {
        searchSuggest.innerHTML = '';
    }
    });

function displayResults(aEvent, aResults) {
    searchSuggest.innerHTML = '';

    if (aResults.length > 0) {
        aResults.forEach(function(aResult) {
            var option = document.createElement('option');
            option.value = aResult;
            searchSuggest.appendChild(option);
        });

        var selectedValue = aEvent.target.value;
        if (aResults.includes(selectedValue)) {
            window.location.href = '?route=product0/search&q=' + encodeURIComponent(selectedValue);
        }
    } else {
        searchSuggest.innerHTML = '';
    }
}
