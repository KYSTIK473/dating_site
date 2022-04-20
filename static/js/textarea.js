const textArea = document.querySelectorAll('.about_register');
textArea.forEach(item => {
    let textAreaH = item.offsetHeight;

    item.addEventListener('input', event => {
        let $this = event.target;

        $this.style.height = textAreaH + 'px';
        $this.style.height = $this.scrollHeight + 'px';
    });
});


function download(input) {
    let wrapper = document.getElementById('ava_img');
    var fileName = input.value;
    console.log(fileName);
        var idxDot = fileName.lastIndexOf(".") + 1;
        var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
        if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){
    try {
        let file = input.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        if (file.name.length > 0) {
            reader.onload = function () {
                wrapper.src = reader.result;
            }
        }
    } catch {
        wrapper.src = 'static/img/1.png';

    }
    }
    else{
            wrapper.src = '/static/img/1.png';
            input.value = null;
            alert("Выберите картинку png/jpg/jpeg!");
        }
}
