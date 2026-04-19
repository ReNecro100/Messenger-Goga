//- - - - - - - - - - - - -
//Подтверждение удаления
//- - - - - - - - - - - - -
try{
    const toDeleteButton = document.querySelector(".delete-user");
    const toModal = document.querySelector(".window");
    const originalHTML = toModal.innerHTML;

    toDeleteButton.onclick = function(e) {
        toModal.innerHTML = `
            <div class="window-name"><img src="https://pngimg.com/d/recycle_bin_PNG11.png"> Вы точно хотите это сделать?</div>
            <div class="window-content">
                <form method="POST">
                    <button type="submit" name="delete_user">Да</button>
                </form>
                <a href="/{% url 'wsschat' 1 %}"><button type="button" class = "no">Нет</button></a>
                <!-- #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC -->
            </div>
        `;
    }

    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('no')) {
            toModal.innerHTML = originalHTML;
        }
    });
}
catch{
    try{
        const toDeleteButton = document.querySelector(".delete-chat");
    const toModal = document.querySelector(".window");
    const originalHTML = toModal.innerHTML;

    toDeleteButton.onclick = function(e) {
        toModal.innerHTML = `
            <div class="window-name"><img src="https://pngimg.com/d/recycle_bin_PNG11.png"> Вы точно хотите это сделать?</div>
            <div class="window-content">
                <form method="POST">
                    <button type="submit" name="delete_chat">Да</button>
                </form>
                <a href="/{% url 'wsschat' 1 %}"><button type="button" class = "no">Нет</button></a>
                <!-- #Pomeniatj idshnik pri zapuske v obraschenije <-VAZHNO SHO KAPEC -->
            </div>
        `;
    }

    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('no')) {
            toModal.innerHTML = originalHTML;
        }
    });
    }
    catch{
        console.log("no comfirmation button?")
    }
}


//- - - - - - - - - - - - -
//Для удаления сообщения через три секунды
//- - - - - - - - - - - - -
function hideDiv() {
var divElement = document.getElementById("messages");
if (divElement) {
    divElement.style.display = "none";
}
}

setTimeout(hideDiv, 3000);


//- - - - - - - - - - - - -
//Для перетаскивания окна
//- - - - - - - - - - - - -
const dragElement = document.querySelector('.window');
const header = document.querySelector('.window-name');

let offsetX, offsetY, isDragging = false;

header.addEventListener('mousedown', (e) => {
    isDragging = true;
    offsetX = e.clientX - dragElement.offsetLeft;
    offsetY = e.clientY - dragElement.offsetTop;
    dragElement.style.cursor = 'grabbing';
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) {
        dragElement.style.position = 'absolute';
        dragElement.style.left = (e.clientX - offsetX) + 'px';
        dragElement.style.top = (e.clientY - offsetY) + 'px';
    }
});

document.addEventListener('mouseup', () => {
    isDragging = false;
    dragElement.style.cursor = '';
});