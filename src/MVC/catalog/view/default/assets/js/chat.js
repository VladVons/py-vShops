/*
Created: 2025.04.03
Author: Vladimir Vons <VladVons@gmail.com>
License: GNU, see LICENSE for more details
*/

class TChatTelegram {
    constructor(aUrl) {
        this.Url = aUrl;
        this.RetryInterval = 10*1000;
        this.Socket = null;
        this.UserChat = null;

        this.elChatContainer = document.getElementById('chat-container');
        this.elMessage = document.getElementById('message');
        this.elName = document.getElementById('chat-name');
        this.elPhone = document.getElementById('chat-phone');

        this.StorageInit();
    }

    StorageInit() {
        const UserChat = localStorage.getItem('user_chat')
        if (UserChat) {
            this.UserChat = JSON.parse(UserChat);
            if (this.UserChat.display) {
                //this.Show(true);
            }

            if (this.UserChat.name) {
                this.elName.value = this.UserChat.name;
                this.elPhone.value = this.UserChat.phone;
            }
        }else{
            this.UserChat = {
                id: Math.random().toString(36).substr(2, 4),
                ip: this.getIpAddress(),
                date: Date.now(),
                user_agent: navigator.userAgent,
                display: false,
                name: '',
                phone: ''
            };
            this.StorageSave();
        }
    };

    StorageSave() {
        localStorage.setItem('user_chat', JSON.stringify(this.UserChat));
    }

    RestoreMessages(aMessages) {
        let PrevDate = null;
        for (const xMessage of aMessages) {
            const Date = xMessage['date'].substring(0, 10);
            if (PrevDate != Date) {
                PrevDate = Date;
                this.addMessage(Date, 'chat-date');
            }

            if (xMessage['text'].startsWith('~')) {
                this.addMessage(xMessage['text'].substring(1), 'chat-user');
            }else{
                this.addMessage(xMessage['text'], 'chat-manager');
            }
        }
    };

    getIpAddress() {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", "https://api64.ipify.org?format=json", false);
        xhr.send();

        if (xhr.status == 200) {
            let ipAddress = JSON.parse(xhr.responseText).ip;
            return ipAddress;
        }
    };

    Connect() {
        this.Socket = new WebSocket(this.Url);

        this.Socket.onopen = () => {
            console.log('WebSocket onopen()');

            this.Socket.send(
                JSON.stringify({
                    type: 'onopen',
                    user_chat: this.UserChat
                })
            );
        };

        this.Socket.onmessage = (event) => {
            console.log('WebSocket onmessage()');

            const data = JSON.parse(event.data);
            if (data.type == 'onopen') {
                this.clearMessage();
                this.RestoreMessages(data.messages);
            }else{
                this.addMessage(data.text, 'chat-manager');
            }
        };

        this.Socket.onerror = (error) => {
            console.log(`WebSocket onerror(): ${error}`);
        };

        this.Socket.onclose = () => {
            console.log('WebSocket onclose(). Retry ...');
            setTimeout(() => this.Connect(), this.RetryInterval);
        };
    };

    postMessage(aText) {
        if (this.Socket.readyState == WebSocket.OPEN) {
            this.Socket.send(
                JSON.stringify({
                    type: 'message',
                    user_chat: this.UserChat,
                    message: aText
                })
            );
            return true;
        } else {
            console.error('Unable to send message via WebSocket');
        };
    };

    sendMessage(aEvent) {
        aEvent.preventDefault();

        const message = this.elMessage.value.trim();
        if (message == '') {
            return;
        }

        if (this.UserChat.name == '') {
            this.UserChat.name = this.elName.value;
            this.UserChat.phone = this.elPhone.value;
            const Contacts = '👤' + this.elName.value + '\n📞' + this.elPhone.value+ '\n🌐' + this.elPhone.ip;
            if (this.postMessage(Contacts)) {
                this.addMessage(Contacts, 'chat-user');
                this.StorageSave();
            }
        };

        if (this.postMessage(message)) {
            this.addMessage(message, 'chat-user');
            this.elMessage.value = '';
        };
    };

    addMessage(aText, aSender) {
        const chatBox = document.getElementById('chat-box');
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', aSender);
        messageDiv.innerHTML = aText.replace(/\n/g, '<br>');
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    clearMessage() {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = '';
    };

    Toggle() {
        const Visible = (this.elChatContainer.style.display == 'none' || this.elChatContainer.style.display == '');
        this.Show(Visible);

        this.UserChat.display = Visible;
        this.StorageSave();
    }

    Show(aVisible) {
        this.elChatContainer.style.display = aVisible ? 'block' : 'none';
    }
}
