/*
Created: 2023.11.20
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/


function showTooltip(aMsg, aId = null) {
    const tooltip = document.createElement("div")
    tooltip.classList.add("tooltip")
    tooltip.textContent = aMsg
    if (aId) {
        const element = document.getElementById(aId)
        const rect = element.getBoundingClientRect()

        /*
        // ToDo. extra width
        tooltip.style.left = rect.left + 'px'
        tooltip.style.top = (rect.top + rect.height) + 'px'
        tooltip.style.right = 0
        console.log(tooltip.style.width)
        */
    }

    document.body.appendChild(tooltip)

    // apply the initial styles
    tooltip.offsetWidth

    tooltip.classList.add("active")

    setTimeout(function () {
        tooltip.classList.remove("active")
        setTimeout(function () {
            document.body.removeChild(tooltip)
        }, 300)
    }, 2000)
}
