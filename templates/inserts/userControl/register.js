function register(){
    let data = new FormData($("#registerForm")[0]);
    fetch("/register", { method: "POST", body: data})
        .then(res => res.text())
        .then(response => {
            let resp = JSON.parse(response)
            if (resp["ANS"] == "YES") { window.location.href = "/pagrindinis"; }
            else { $("#registerError")[0].innerHTML = "<b>" + resp["ERROR"] + "</b>"; }});
    return false;
}