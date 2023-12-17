/*
Created: 2023.11.13
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function goToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

window.onscroll = function() {
    const scrollPosition = document.documentElement.scrollTop || document.body.scrollTop
    const goTopBtn = document.getElementById('viBtnGoTop')

    if (scrollPosition > 200) {
        goTopBtn.style.display = 'block'
    } else {
        goTopBtn.style.display = 'none'
    }
}
