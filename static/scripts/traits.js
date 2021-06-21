
const listOfTraits = ["playful", "aggressive" , "curious" , "social" , "demanding", "dominant" , "protective" , "apartment", "vocal"]
const checked = [0,0,0,0,0,0,0,0,0];
function setChecked(name){
    switch(name){
        case "playful":
            checked[0] = 1;
            break;
        case "aggressive":
            checked[1] = 1;
            break;
        case "curious":
            checked[2] = 1;
            break;
        case "social":
            checked[3] = 1;
            break;
        case "demanding":
            checked[4] = 1;
            break;
        case "dominant":
            checked[5] = 1;
            break;
        case "protective":
            checked[6] = 1;
            break;
        case "apartment":
            checked[7] = 1;
            break;
        case "vocal":
            checked[8] = 1;
            break;
    }
}

var disabled = true;

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
        setChecked(currentRow);
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

        let allChecked = true;
        for(var g=0; g<10; g++){
            if(checked[g] === 0){
                allChecked = false;
            }
        }
        if(allChecked){
            btn = document.getElementById("add-puppy-submit-btn");
            btn.disabled = false;
            alertCheck = document.getElementById("p-select-alert");
            alertCheck.style.display = "none";
        } else{
            btn.disabled = true;
        }
    }

})

})





    




