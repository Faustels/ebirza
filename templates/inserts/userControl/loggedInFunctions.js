function logout(){
    fetch("/logout", { method:"POST"})
        .then(res => {location.reload();});
    return false;
}