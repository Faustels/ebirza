
document.addEventListener("mousemove", changeTooltip);
function toFront(object){
    document.getElementById("mapFrontRegion").innerHTML = object.innerHTML
    document.getElementById("mapFrontRegion").onclick = object.onclick
    document.getElementById("mapFrontRegion").tooltipText = "<b>" + object.id + "</b>"
    showTooltip(object)
}
function showTooltip(object) {
    document.getElementById("customTooltip").style.display = 'block'
    document.getElementById("customTooltip").innerHTML = object.tooltipText
}
function hideTooltip(){
    document.getElementById("customTooltip").style.display = 'none'
}
function changeTooltip(e){
    document.getElementById("customTooltip").style.top = (e.clientY).toString() + "px"
    document.getElementById("customTooltip").style.left = (e.clientX + 20).toString()  + "px"
}

function clickRegion(object){
    console.log("test")
}