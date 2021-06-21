const ham = document.getElementById('hamburger')
ham.title = "notclicked"

ham.onclick = () => {
    const top = document.getElementById('ham-1');
    const middle = document.getElementById('ham-2');
    const bottom = document.getElementById('ham-3');
    const nav = document.getElementById('sidenavbar')

    if(ham.title === "notclicked"){
        top.style.transform = "rotate(135deg) translateY(-15px)"
        bottom.style.transform = "rotate(-135deg) translateY(15px)"
        middle.style.display = "none";
        nav.style.left = 0;
        ham.title = "clicked";
        
    }

    else if(ham.title === "clicked"){
        top.style.transform = "rotate(0deg) translateY(0px)";
        middle.style.display = "block";
        bottom.style.transform = "rotate(0deg) translateY(0px)";
        ham.title = "notclicked";
        nav.style.left = "-100%";
    }
    
    
}