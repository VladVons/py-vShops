/*
opyright:    Vladimir Vons, UA
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2022.05.15-2
*/


function Btn_GetSchemeEmpty() {
    HttpRequest(
        '/api/get_scheme_empty',
        function(aData) {
            console.log('aData', aData);
            let Dbl = new TDbList(aData['data']['data']);
            let Rec = Dbl.Shuffle();
            document.getElementById('url0').value = Rec.GetField('url');
            document.getElementById('script').value = '';
          },
        {'cnt': 20}
    );
};

function InsertAtCaret(aTextArea, aText) {
    aTextArea.setRangeText(
        aText,
        aTextArea.selectionStart,
        aTextArea.selectionEnd,
        'end'
    );
}

function ClearObj(aTagName) {
    let Items = document.getElementsByTagName(aTagName);
    for (let i = 0; i < Items.length; i++) {
        if (Items[i].type.startsWith('text')) {
            Items[i].value = '';
        }
    }
}

function Btn_GoUrl(aField) {
    let Url = document.getElementById(aField).value;
    if (Url) {
        window.open(Url, '_blank').focus();
    }else{
        alert('Url is empty');
    }
};

function InsertTab(aThis, aEvent) {
    if (aEvent.keyCode == 9) {
        aEvent.preventDefault()

        aThis.setRangeText(
            '  ',
            aThis.selectionStart,
            aThis.selectionStart,
            'end'
        );
    }
};

