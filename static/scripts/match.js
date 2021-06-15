const elemId = document.getElementsByClassName('active shown')[0].id;

document.getElementsByClassName('active shown')[0].onclick = () => {
    window.location.href="http://127.0.0.1:5000/dog/"+ elemId
}


function findNext(){
    const active = document.getElementsByClassName('active shown')[0];
    active.className = 'matching-dog inactive shown';
    const newElem = document.getElementsByClassName('inactive notshown')[0];
    newElem.className = 'matching-dog active shown';
    const elemId = document.getElementsByClassName('active shown')[0].id;

    document.getElementsByClassName('active shown')[0].onclick = () => {
        window.location.href="http://127.0.0.1:5000/dog/"+ elemId
    }

}
   
    