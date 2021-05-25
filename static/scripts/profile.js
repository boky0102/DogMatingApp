console.log("radi");

const imgInp = document.getElementById("image-inpt");
imgInp.onchange = evt => {
    const exists = document.getElementById('preview');
    if(exists !== null){
        exists.remove();
        }
    const [file] = imgInp.files
    if (file) {
        const container = document.getElementById('avatar')
        const preview = document.createElement('img');
        preview.id = "preview";
        preview.src = URL.createObjectURL(file);
        preview.style.height = "100%";
        preview.style.width = "100%";
        preview.style.objectFit = "cover";
        /* preview.style.maxWidth = "100%"; */
        preview.style.borderRadius = "50%";
        container.appendChild(preview);
    }
}