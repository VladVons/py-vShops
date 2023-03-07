/*
opyright:    Vladimir Vons, UA
Author:      Vladimir Vons <VladVons@gmail.com>
Created:     2022.04.10
*/


function HttpRequest(aUrl, aFunc, aPostJson = null) {
    console.log('HttpRequest()', aUrl, aPostJson);

    let xhr = new XMLHttpRequest();
    if (aPostJson) {
        xhr.open('post', aUrl);
        xhr.setRequestHeader('Content-Type', 'application/json');
    } else {
        xhr.open('get', aUrl);
    }

    xhr.onload = function() {
        if (xhr.status == 200) {        
            //console.log('HttpRequest().OnLoad()', xhr.responseText);
            let Data = JSON.parse(xhr.responseText);
            aFunc(Data);
        } else {
            console.log('Server error ' + xhr.status);
        }
    }

    xhr.onerror = function() {
        console.log('Connection error');
    }

    if (aPostJson) {
        var aPostJson = JSON.stringify(aPostJson);
    }
    xhr.send(aPostJson);
}


class TWebSock {
    constructor() {
        this.Debug = false;
        this.Id = Math.random().toString(16).slice(2);
    };

    Log(aMsg) {
        if (this.Debug) {
            console.log(aMsg);
        }
    }

    Connect(aUrl) {
        let This = this;
        this.Log('Connect ' + aUrl)

        this.ws = new WebSocket(aUrl);

        this.ws.onerror = function(aEvent) {
            alert('Err: ' + aUrl);
        };

        this.ws.onmessage = function(aEvent) {
            let Data = JSON.parse(aEvent.data);
            This.OnMessage(aEvent, Data);
        };

        this.ws.onclose = function() {
            This.Log('OnClose');
        };
    };

    ConnectPlugin(aName) {
        let Url = 'ws://' + window.location.host + '/ws/?plugin=' + aName + '&id=' + this.Id;
        this.Connect(Url)
    }

    ConnectId() {
        let Url = 'ws://' + window.location.host + '/ws/?id=' + this.Id;
        this.Connect(Url)
    }

    Call(aParam) {
        let Data = JSON.stringify({'param': aParam});
        //this.ws.send(Data);
        this.ws.onopen = () => this.ws.send(Data);
    };

    OnClose() {
        this.Log('OnClose');
    };

    OnMessage(aEvent) {
        this.Log('OnMessage');
    };
};
