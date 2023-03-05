$().ready(function() {
    let classicTime = document.getElementById('classicTime')
    classicTime.innerText = classicTime.innerText.toString().timeTextFormat();

    let educationalTime = document.getElementById('educationalTime')
    educationalTime.innerText = educationalTime.innerText.toString().timeTextFormat();
    
    let timeLimitedTime = document.getElementById('timeLimitedTime')
    timeLimitedTime.innerText = timeLimitedTime.innerText.toString().timeTextFormat();
})