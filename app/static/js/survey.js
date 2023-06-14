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

    let includedRadio = document.getElementsByName('included');
    let nameAndSurnameFields = document.getElementsByClassName('included-visibility')

    for (let i = 0; i < includedRadio.length; i++) {
        includedRadio[i].addEventListener('change', function () {
            if (this.value === 'Yes') {
                for (let j = 0; j < nameAndSurnameFields.length; j++) {
                    nameAndSurnameFields[j].style.display = ''
                }
            } else {
                for (let j = 0; j < nameAndSurnameFields.length; j++) {
                    nameAndSurnameFields[j].style.display = 'none'
                }
            }
        })
    }

});