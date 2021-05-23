console.log("radi");

const imgInp = document.getElementById("actual-btn");
imgInp.onchange = evt => {
    const exists = document.getElementById('preview');
    if(exists !== null){
        exists.remove();
        }
    const [file] = imgInp.files
    if (file) {
        const container = document.getElementById('image-upload-wrap')
        const preview = document.createElement('img');
        preview.id = "preview";
        preview.src = URL.createObjectURL(file);
        preview.style.height = "100%";
        preview.style.width = "100%";
        preview.style.objectFit = "cover";
        /* preview.style.maxWidth = "100%"; */
        preview.style.borderRadius = "15px";
        container.appendChild(preview);
    }
}
    
