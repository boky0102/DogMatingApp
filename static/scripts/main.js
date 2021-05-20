console.log("Uspio")

function handleRegClick(){
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    loginForm.style.display = "none";
    registerForm.style.display = "flex";
}

function handleRegBackClick(){
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    loginForm.style.display = "flex";
    registerForm.style.display = "none";
}

function handlePasswordValue(){
    const firstPass = document.getElementById('first-pass');
    const seconPass = document.getElementById('second-pass');
    const alert = document.getElementById('password-alert');
    const regButton = document.getElementById('reg-btn');
    const username = document.getElementById('form-usr');
    var alertMsg = "";
    console.log(username.value.length);
    if(username.value.length < 4 && username.value !== undefined){
        alertMsg = "Username must be longer than 4 characters";
        document.getElementById("alert-text").innerHTML = alertMsg;
        alert.style.display = 'block';
        regButton.disabled = true;
    }
    else if(firstPass.value.length < 6 && username.value !== undefined){
        alertMsg = "Password must be longer than 6 characters";
        alert.style.display = "block";
        regButton.disabled = true;
    }
    else{
        alert.style.display = 'none'
    }

    console.log(firstPass.value, seconPass.value);

    if(firstPass.value !== "" && seconPass.value !== ""){
        if(firstPass.value === seconPass.value){
            alert.style.display = 'none';
            regButton.disabled = false;
        }
        else if((firstPass.value === "" || undefined) || (seconPass.value === "" || undefined)){
            alert.style.display = 'none';
        }
        
        else{
            alertMsg = "Passwords don't match";
            alert.style.display = 'block';
            regButton.disabled = true;
        }

    }

    
    document.getElementById("alert-text").innerHTML = alertMsg;
    
}