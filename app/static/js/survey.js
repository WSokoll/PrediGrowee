$().ready(function () {
    let educationSelect = document.getElementById('education');
    let educationOtherDiv = document.getElementById('education-other-visibility');

    educationSelect.onchange = function () {
        if (educationSelect.value === 'other') {
            educationOtherDiv.style.display = '';
        } else {
            educationOtherDiv.style.display = 'none';
        }
    };
});