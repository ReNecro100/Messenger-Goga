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