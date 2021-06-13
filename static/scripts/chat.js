

function getMessages(){
    url = window.location.href;
    currentConID = url.split('/')[5];
    fetch("http://127.0.0.1:5000/"+currentConID+"/chat").then( res => res.json())
    .then((data) => {

        const messages = document.querySelectorAll(".message-wrap")
        const messages2 = document.querySelectorAll(".message-wrap-nonholder")

        if(messages.length + messages2.length !== data.length){
            const messagesParent = document.getElementById('messages')
            for(var j=messages.length + messages2.length; j<data.length; j++){
                const messageWrap = document.createElement('div');

                if(data[j].type === "holder"){
                    messageWrap.className = 'message-wrap';
                }
                else{
                    messageWrap.className = 'message-wrap-nonholder';
                }

                const avatar = document.createElement('img');
                avatar.className = "message-avat";
                avatar.src = data[j].avat;

                const avatarHolder = document.createElement('div');
                avatarHolder.className = "message-avat-holder";
                avatarHolder.appendChild(avatar);

                messageWrap.appendChild(avatarHolder);

                const messageData = document.createElement('div');
                messageData.className = 'message-data';
                messageData.textContent = data[j].message;
                console.log(data[j]);
                messageWrap.appendChild(messageData);
                messagesParent.appendChild(messageWrap);
            }
        }
        
    })
    .catch(err => console.log(err))
}

getMessages();

setInterval(getMessages, 10000);
