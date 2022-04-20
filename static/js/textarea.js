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
    try {
        let file = input.files[0];
        let reader = new FileReader();
        reader.readAsDataURL(file);
        let wrapper = document.getElementById('ava_img');
        if (file.name.length > 0) {
            reader.onload = function () {
                wrapper.src = reader.result;
            }
        }
        else {
            wrapper.src = 'static/img/1.png';
        }
    } catch {
        let wrapper = document.getElementById('ava_img');
        wrapper.src = 'static/img/1.png';

    }
}
