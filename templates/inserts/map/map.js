
document.addEventListener("mousemove", changeTooltip);
currentSelector = ""
function toFront(object){
    $("#mapFrontRegion")[0].classList.remove("mapGSelected")
    if (object.classList.contains("mapGSelected")) {
        $("#mapFrontRegion")[0].classList.add("mapGSelected")
    }
    $("#mapFrontRegion")[0].innerHTML = object.innerHTML
    $("#mapFrontRegion")[0].tooltipText = "<b>" + object.id + "</b>"
    $("#mapFrontRegion")[0].currentlySelected = object.id
    showTooltip(object)
}
function showTooltip(object) {
    $("#customTooltip")[0].style.display = 'block'
    $("#customTooltip")[0].innerHTML = object.tooltipText
}
function hideTooltip(){
    $("#customTooltip")[0].style.display = 'none'
}
function changeTooltip(e){
    $("#customTooltip")[0].style.top = (e.clientY).toString() + "px"
    $("#customTooltip")[0].style.left = (e.clientX + 20).toString()  + "px"
}

function clickRegion(object) {
    if (currentSelector == object.currentlySelected) {
        $("#" + object.currentlySelected)[0].classList.remove("mapGSelected")
        currentSelector = ""
    } else {
        if (currentSelector != "") {
            $("#" + currentSelector)[0].classList.remove("mapGSelected")
        }
        $("#" + object.currentlySelected)[0].classList.add("mapGSelected")
        currentSelector = object.currentlySelected
    }
}