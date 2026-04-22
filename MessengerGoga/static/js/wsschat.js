const roomName = JSON.parse(document.getElementById('room-name').textContent);
const user = JSON.parse(document.getElementById('itsname').textContent);
const userid = JSON.parse(document.getElementById('itsid').textContent);

const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const chatSocket = new WebSocket(
    protocol + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const messagesArea = document.getElementById('messages-area');

    if(data.action=='new_message'){
        addmsg(data)
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
    if(data.action=='history'){
        addmsg(data)
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
    else{
        const messageElement = document.querySelector(`.chat-message[data-message-id="${data.message_id}"]`);
        if (messageElement) {
            messageElement.remove();
        }
    }
};

function addmsg(data){
    const existingMessage = document.querySelector(`.chat-message[data-message-id="${data.id}"]`);
    if (existingMessage) {
        return;
    }
    const newDiv = document.createElement('div');
    newDiv.className = 'chat-message';
    newDiv.setAttribute('data-message-id', data.id);
    let msgFile = null
    try{
        msgFile = data.message_file 
    }
    catch{}
    // msgFile ? console.log(msgFile.length) : console.log(data.message);
    if(user == data.username){
        newDiv.innerHTML = `
            <div class="msg-words">
                <p>${data.username}: ${data.message}</p>
                <button class="delete-msg-btn" data-message-id="${data.id}">🗑</button>
            </div>
        ` + (msgFile ? `<img src="${msgFile}" alt="">` : ``)

        const deleteBtn = newDiv.querySelector('.delete-msg-btn');
        if (deleteBtn) {
            deleteBtn.onclick = function(e) {
                e.preventDefault();
                const messageId = this.getAttribute('data-message-id');
                chatSocket.send(JSON.stringify({
                    "type": "delete_message",
                    'action': 'delete_message',
                    'message_id': messageId,
                    'username': user,
                }));
                
                // Удаляем сообщение из DOM
                const messageElement = this.closest('.chat-message');
                if (messageElement) {
                    messageElement.remove();
                }
            };
        }
        // Автоматическая прокрутка вниз
        const messagesArea = document.getElementById('messages-area');
        messagesArea.appendChild(newDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;

    }
    else{
        newDiv.innerHTML = `
            <div class="msg-words">
                <p>${data.username}: ${data.message}</p>
            </div>
        ` + (msgFile ? `<img src="${msgFile}" alt="">` : ``)
        
        // Автоматическая прокрутка вниз
        const messagesArea = document.getElementById('messages-area');
        messagesArea.appendChild(newDiv);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }
}
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};


document.querySelector('#chat-message-submit').onclick = async function(e) {
    const messageInputDom = document.querySelector('#chat-message-input')
    const fileInputDom = document.querySelector('#chat-file-input')
    const message = messageInputDom.value;
    let file = null
    try{
        file = await compressImage(fileInputDom.files[0])
    }
    catch{}

    if (message!="" || file!=null){
        chatSocket.send(JSON.stringify({
            'type': "chat_message",
            'action': 'new_message',
            'message': message,
            'username': user,
            'message_file': file
        }));
        messageInputDom.value = '';
        fileInputDom.value = '';
    }
};

function compressImage(file, maxWidth = 640, maxHeight = 480) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            const img = document.createElement("img");
            
            img.onload = function() {
                const canvas = document.createElement("canvas");
                const ctx = canvas.getContext("2d");
                
                let width = img.width;
                let height = img.height;
                
                if (width > maxWidth) {
                    height = (height * maxWidth) / width;
                    width = maxWidth;
                }
                
                if (height > maxHeight) {
                    width = (width * maxHeight) / height;
                    height = maxHeight;
                }
                
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                
                const dataurl = canvas.toDataURL(file.type, 0.5);
                
                resolve(dataurl);
            };
            
            img.onerror = reject;
            img.src = e.target.result;
        };
        
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

document.body.addEventListener('click', function(e) {
    // Проверяем, что кликнули по кнопке удаления
    if (e.target.classList.contains('delete-msg-btn')) {
        e.preventDefault();
        
        const messageId = e.target.getAttribute('data-message-id');
        
        // Отправляем на сервер
        chatSocket.send(JSON.stringify({
            'action': 'delete_message',
            'message_id': messageId,
            'username': user
        }));
        
        // Удаляем сообщение из DOM
        const messageElement = e.target.closest('.chat-message');
        if (messageElement) {
            messageElement.remove();
        }
    }
});

//Okno dvigatj
// let isDragging = false;
// let currentWindow = null;
// let startX, startY, initialLeft, initialTop;

// document.querySelectorAll('.window').forEach(win => {
//     const header = win.querySelector('.window-name');
    
//     header.addEventListener('mousedown', (e) => {
//         if (e.target.closest('.window-name')) {
//             isDragging = true;
//             currentWindow = win;
            
//             // Запоминаем текущую позицию окна
//             const rect = win.getBoundingClientRect();
//             initialLeft = rect.left;
//             initialTop = rect.top;
//             startX = e.clientX - rect.left;
//             startY = e.clientY - rect.top;
            
//             // Переводим ТОЛЬКО текущее окно в absolute
//             win.style.position = 'absolute';
//             win.style.left = initialLeft + 'px';
//             win.style.top = initialTop + 'px';
//             win.style.margin = '0';
//             // Не меняем размер!
//             win.style.width = rect.width + 'px';
//             win.style.height = rect.height + 'px';
//             win.style.zIndex = '9999';
            
//             // Остальные окна остаются в grid, ничего с ними не делаем
//         }
//     });
// });

// document.addEventListener('mousemove', (e) => {
//     if (isDragging && currentWindow) {
//         currentWindow.style.left = (e.clientX - startX) + 'px';
//         currentWindow.style.top = (e.clientY - startY) + 'px';
//     }
// });

// document.addEventListener('mouseup', () => {
//     if (isDragging) {
//         // Окно остаётся там, где его отпустили
//         // Ничего не возвращаем
//         isDragging = false;
//         currentWindow = null;
//     }
// });