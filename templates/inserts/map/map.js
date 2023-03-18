
document.addEventListener("mousemove", changeTooltip);
currentSelector = ""
tooltip = $("#customTooltip")[0]
mapFront = $("#mapFrontRegion")[0]
SetColors(sunHours)
function toFront(object){
    mapFront.innerHTML = object.innerHTML
    mapFront.currentlyFront = object.id
    mapFront.tooltipText = "<b>" + object.id + "</b>" + "<p>" + sunHours[object.id].toString() + "val. per metus" + "</p>"
    showTooltip(object)
}
function showTooltip(object) {
    tooltip.style.display = 'block'
    tooltip.innerHTML = object.tooltipText
}
function hideTooltip(){
    tooltip.style.display = 'none'
}
function changeTooltip(e){
    tooltip.style.top = (e.clientY).toString() + "px"
    tooltip.style.left = (e.clientX + 20).toString()  + "px"
}

function clickRegion(object) {
    if (currentSelector === object.currentlyFront) {
        $("#" + object.currentlyFront)[0].classList.remove("mapGSelected")
        currentSelector = ""
    } else {
        if (currentSelector !== "") {
            $("#" + currentSelector)[0].classList.remove("mapGSelected")
        }
        $("#" + object.currentlyFront)[0].classList.add("mapGSelected")
        currentSelector = object.currentlyFront
    }
}

function SetColors(values) {
    let max = 0
    let min = 366 * 24

    for (let key in values) {
        if (values[key] < min) {
            min = values[key]
        }
        if (values[key] > max) {
            max = values[key]
        }
    }

    for (let key in values) {
        $("#" + key)[0].style.fill = getColor((values[key] - min) / (max - min))
    }
}

function getColor(amount) {
    let maxColorG = 90
    let maxColorB = 85
    let minColorG = 225
    let minColorB = 160


    let ats = "#F5" + Math.round(minColorG - (minColorG - maxColorG) * amount).toString(16)
        + Math.round(minColorB - (minColorB - maxColorB) * amount).toString(16)
    return ats
}