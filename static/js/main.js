// Variables
var messages = document.querySelector('.message-list')
var btn = document.querySelector('.btn')
var input = document.querySelector('input')

// Button/Enter Key
btn.addEventListener('click', sendMessage)
input.addEventListener('keyup', function (e) { if (e.keyCode == 13) sendMessage() })

// History Function
function loadHistory() {
    fetch(
        '/history'
    ).then(
        response => response.json()
    ).then(
        data => {
            for (let i = 9; i < data.length; i++) {
                if (data[i].role == 'user') {
                    writeLine(`User: ${data[i].content}`, 'primary')
                } else {
                    writeLine(`Tsukushi Futaba: ${data[i].content}`, 'secondary')
                }
            }
        }
    ).catch(
        error => console.error('Error: ', error)
    )
}

loadHistory()

// Messenger Functions
function sendMessage() {
    var msg = input.value;
    writeLine(`User: ${msg}`, 'primary')

    input.value = ''
    fetch(
        '/chat',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'message': msg})
        }
    ).then(
        response => response.json()
    ).then(
        data => addMessage(data, 'secondary')
    ).catch(
        error => console.error('Error: ', error)
    )
}

function addMessage(msg, typeMessage = 'primary') {
    writeLine(`${msg.FROM}: ${msg.MESSAGE}`, typeMessage)
}

function writeLine(text, typeMessage) {
    var message = document.createElement('li')
    message.classList.add('message-item', 'item-'+typeMessage)
    message.innerHTML = text
    messages.appendChild(message)
    messages.scrollTop = messages.scrollHeight;
}