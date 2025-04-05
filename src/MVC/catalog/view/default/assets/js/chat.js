const BOT_TOKEN = "YOUR_BOT_TOKEN";
const CHAT_ID = "YOUR_CHAT_ID";

function toggleChat() {
    let chatBox = document.getElementById("chat-container");
    chatBox.style.display = (chatBox.style.display === "none" || chatBox.style.display === "") ? "block" : "none";
}

function sendMessage() {
    let message = document.getElementById("message").value;
    if (message.trim() === "") return;

    addMessage(message, "user");

    // Надіслати повідомлення до Telegram API
    fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: CHAT_ID, text: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            addMessage("Message sent to bot!", "bot");
        } else {
            addMessage("Error sending message!", "bot");
        }
    });

    document.getElementById("message").value = "";
}

function addMessage(text, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
