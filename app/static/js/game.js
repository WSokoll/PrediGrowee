
$().ready(function() {
    $(".tooltip-icon").tooltip()

    // Warning modal
    if (document.getElementById('warningModal') !== null) {
        $('#warningModal').modal('show');
    }

    function setScreenSize () {
        let screenSizeInput = document.getElementById('screen_size');
        screenSizeInput.value = window.innerWidth.toString() + 'x' + window.innerHeight.toString();
    }

    // On submit function - two different submit buttons
    $('#prediction-form').on('submit', function () {
         setScreenSize();

         let buttonId = $(document.activeElement).attr('id');
         let showResultsInput = document.getElementById('show_results');
         showResultsInput.value = buttonId === 'btn-results';

         return true;
    });

    // Time-limited mode
    let mode = $('#mode').data().name;
    if (mode === 'time-limited') {
        let timeLimit = $('#timeLimit').data().name;
        let cdAlert = document.getElementById('countDownAlert');

        let secondsLeft = timeLimit - 1;
        setInterval(function () {
            cdAlert.innerHTML = 'You are in time-limited mode. You have <b>' + secondsLeft.toString() +
                                '</b> seconds left to answer before next case appears.';
            secondsLeft -= 1;
        }, 1000)

        setTimeout(function () {
            setScreenSize();

            let showResultsInput = document.getElementById('show_results');
            showResultsInput.value = false;

            document.getElementById('prediction-form').submit();
        }, timeLimit * 1000)
    }

});

// Sidebar transition on/off
function transitionOn(on) {
    let offcanvas = document.getElementsByClassName('offcanvas');
    for (let i = 0; i < offcanvas.length; i++) {
        offcanvas[i].style['transition-duration'] = on ? '.3s' : '0s';
    }
}