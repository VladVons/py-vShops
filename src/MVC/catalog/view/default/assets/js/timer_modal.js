/*
Created: 2023.11.10
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/

document.addEventListener('DOMContentLoaded', function() {
    const Min = 200 * 1000
    const Max = 300 * 1000
    const Delay = Math.random() * (Max - Min) + Min
    setTimeout(function() {
        const Modal = new bootstrap.Modal(document.getElementById('viTimerModal'))
        Modal.show()
    }, Delay)
})
