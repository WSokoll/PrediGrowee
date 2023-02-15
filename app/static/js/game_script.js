
$().ready(function() {
    // Warning modal
    if (document.getElementById('warningModal') !== null) {
        $('#warningModal').modal('show');
    }

    // On submit function - two different submit buttons
    $('#prediction-form').on('submit', function () {
         let screenSizeInput = document.getElementById('screen_size');
         screenSizeInput.value = window.innerWidth.toString() + 'x' + window.innerHeight.toString();

         let buttonId = $(document.activeElement).attr('id');
         let showResultsInput = document.getElementById('show_results');
         showResultsInput.value = buttonId === 'btn-results';

         return true;
    });
});

// Sidebar transition on/off
function transitionOn(on) {
    let offcanvas = document.getElementsByClassName('offcanvas');
    for (let i = 0; i < offcanvas.length; i++) {
        offcanvas[i].style['transition-duration'] = on ? '.3s' : '0s';
    }
}