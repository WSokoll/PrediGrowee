$().ready(function() {
    let timeElements = document.getElementsByClassName('resultTimeSpent');

    for (let i = 0; i < timeElements.length; i++) {
        timeElements.item(i).innerHTML = timeElements.item(i).innerHTML.toString().timeTextFormat();
    }
})