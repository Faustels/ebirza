
var assistantMessageBox = $("#assistantMessageBox")[0];
var assistantTextBox = $("#assistantTextBox")[0];

assistantTextBox.onkeyup = function(e){
    if (e.keyCode == 13){
        sendAssistantMessage();
    }
}
function sendAssistantMessage(){
    if (assistantTextBox.value == ""){ return;}
    fetch("/assistant?text=" + assistantTextBox.value, { method:"GET" })
        .then(res => res.text())
        .then(response => {
            assistantMessageBox.innerHTML += addToBox(assistantTextBox.value, true)
            assistantMessageBox.innerHTML += addToBox(response, false);
            assistantTextBox.value = "";
            assistantMessageBox.scrollTop = assistantMessageBox.scrollHeight;
            });
    return false;
}

function addToBox(text, isUser){
    let ans = "<div class='assistantMessage "
    if (isUser){
        ans += "assistantUserMessage";
    }
    else{
        ans += "assistantBotMessage";
    }
    ans += "'>"
    ans += text
    ans += "</div>"
    return ans
}