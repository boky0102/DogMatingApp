function goBack(){
    window.history.back();
}


const background = document.getElementById("mod-backg")


const contactButton = document.getElementById("contact")

const closeButton = document.getElementById("close-icon")

contactButton.onclick = () => {
    background.style.visibility = "visible";
    background.style.opacity = 1;
}

closeButton.onclick = () => {
    background.style.visibility = "hidden";
    background.style.opacity = 0;
}



