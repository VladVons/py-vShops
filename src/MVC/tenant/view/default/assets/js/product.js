/*
Created: 2023.12.27
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/

const formMain = new TFormChangeTracker('viFormMain', 'vChanged')
document.getElementById('viBtnMainSave').onclick = () => formMain.submit()

const formImage = new TFormChangeTracker('viFormImage', 'vChanged')
document.getElementById('viBtnImageSave').onclick = () => formImage.submit()

//const formProduct0 = new TFormChangeTracker('viFormProduct0', 'vChanged')
//document.getElementById('viBtnProduct0Save').onclick = () => formProduct0.submit()

const chkEnabled = document.getElementById("chk_enabled")
chkEnabled.onclick = function(event) {
    formMain.setReadonly(!event.target.checked)
    event.target.style.pointerEvents = 'auto'
}

document.addEventListener('DOMContentLoaded', function() {
    formMain.setReadonly(!chkEnabled.checked)
    chkEnabled.style.pointerEvents = 'auto'
})

function OnClickCategory(aId, aTitle) {
    document.getElementById('viCategoryId').value = aId
    document.getElementById('viCategoryTitle').value = aTitle
}

const param = {
    selector: 'viCategory',
    items: 'viCategoryItems',
    url: gData.getValue('href/category_ajax')
}
document.getElementById('viCategoryMenu').onclick = () => OnClickDropdownMenu(param)

initDropdownMenu({selector: 'viCategory'})
