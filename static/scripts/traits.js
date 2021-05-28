
const listOfTraits = ["playful", "aggressive" , "curious" , "social" , "demanding", "dominant" , "protective" , "apartment", "vocal"]

listOfTraits.forEach((currentRow) => {

    var currentWrap = document.getElementById(currentRow);

    const boxes = currentWrap.querySelectorAll(".rating-box");

    var locked = false;


    currentWrap.onmouseout = evt => {
        if( locked === false ){
            for(var i=1; i<11; i++){
                var id = currentRow + "-" + i;
                var currBox = document.getElementById(id);
                currBox.style.backgroundColor = "rgba(255,255,255, 0.4)";
            }
        }
        else if( locked === true ){
            for(var i=1; i<11; i++){
                var id = currentRow + "-" + i;
                var currBox = document.getElementById(id);
                if(currBox.title === "!range"){
                    currBox.style.backgroundColor = "rgba(255,255,255, 0.4)";
                }
                else{
                    currBox.style.backgroundColor = "#2ecc71";
                }
                
                
            }
        }  
    }

    boxes.forEach((box) =>{
    console.log(box);
    box.onmouseover = evt => {
        const selectedId = box.id.split("-")[1];
        for(var i=0; i<selectedId; i++){
            var currentId = currentRow + "-" + (i+1);
            let currentBox = document.getElementById(currentId);
            currentBox.style.backgroundColor = "#2ecc71";
            currentBox.style.cursor = "pointer";
        }
    }

    box.onclick = evt => {
        locked = true;
        currId = box.id.split("-")[1];
        const currentValue = document.getElementById(currentRow + "-input");
        currentValue.value = currId;
        for(var j=1; j < 11; j++){
            var curBox = document.getElementById(currentRow + "-" + j);
            if(j <= currId){
                curBox.style.backgroundColor = "#2ecc71";
                curBox.title = "";
            }
            else{
                curBox.style.backgroundColor ="rgba(255,255,255, 0.4)";
                curBox.title = "!range"
            }
        }
    }

})

})

    




