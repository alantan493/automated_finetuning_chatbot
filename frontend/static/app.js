class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.messages = [];
    }

    display() {
        const { chatBox, sendButton } = this.args;

        // Set chatbox to active on load
        chatBox.classList.add('chatbox--active');

        // Send button event listener
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        // Listen for "Enter" key in the input field
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);

        // Updated fetch request to your backend
        // https://httpsee3180-smapps2webappchatbot.com/chatbot/send
        // http://127.0.0.1/chatbot/send
        fetch('https://httpsee3180-smapps2webappchatbot.com/chatbot/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text1 }),  // Send user input (text1) to the backend
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                this.messages.push({ name: "Chatbot", message: data.message });
            } else {
                this.messages.push({ name: "Chatbot", message: "No response from the chatbot." });
            }
            this.updateChatText(chatbox);
            textField.value = '';  // Clear input field
        })
        .catch((error) => {
            console.error('Error:', error);
            this.messages.push({ name: "Chatbot", message: "Error occurred, please try again." });
            this.updateChatText(chatbox);
            textField.value = '';
        });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item) {
            if (item.name === "Chatbot") {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>';
            } else {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>';
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

// Instantiate the Chatbox class and display the chat
const chatbox = new Chatbox();
chatbox.display();
