
function traitHandler(){


    var currentWrap = document.getElementById("playful");

    const boxes = currentWrap.querySelectorAll(".rating-box");

    var locked = false;


    currentWrap.onmouseout = evt => {
        if( locked === false ){
            for(var i=1; i<11; i++){
                var id = "playful-" + i;
                var currBox = document.getElementById(id);
                currBox.style.backgroundColor = "rgba(255,255,255, 0.4)";
            }
        }  
    }

    boxes.forEach((box) =>{
    console.log(box);
    box.onmouseover = evt => {
        const selectedId = box.id.split("-")[1];
        for(var i=0; i<selectedId; i++){
            var currentId = "playful-" + (i+1);
            let currentBox = document.getElementById(currentId);
            currentBox.style.backgroundColor = "green";
            currentBox.style.cursor = "pointer";
        }
    }

    box.onclick = evt => {
        locked = true;
        currId = box.id.split("-")[1];
        for(var j=1; j < 11; j++){
            var curBox = document.getElementById("playful-"+j);
            if(j <= currId){
                curBox.style.backgroundColor = "green";
            }
            else{
                curBox.style.backgroundColor ="rgba(255,255,255, 0.4)";
            }
        }
    }

})

}

traitHandler();

