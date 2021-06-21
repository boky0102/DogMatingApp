

function handleAcceptClick(clickedID){
    const values = clickedID.split("-");
    idElem = document.getElementById("curId");
    typeElem = document.getElementById("requestType")
    idElem.value = values[1];
    typeElem.value = values[0];
    
}

console.log("LALALAL")