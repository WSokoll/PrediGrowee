String.prototype.timeTextFormat = function () {
    let sec_num = parseInt(this, 10);
    let hours   = Math.floor(sec_num / 3600);
    let minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    let seconds = sec_num - (hours * 3600) - (minutes * 60);

    let finalString = '';

    if (hours === 1) {
        finalString = '1 hour';
    } else if (hours > 1) {
        finalString = hours.toString() + ' hours';
    }

    if (hours > 0 && minutes > 0 && seconds > 0) {
        finalString += ', ';
    } else if (hours > 0 && minutes > 0) {
        finalString += ' and ';
    }

    if (minutes === 1) {
        finalString += '1 minute';
    } else if (minutes > 1){
        finalString += minutes.toString() + ' minutes';
    }

    if (finalString !== '') {
        finalString += ' and '
    }

    if (seconds === 1) {
        finalString += '1 second';
    } else if (seconds > 1) {
        finalString += seconds.toString() + ' seconds';
    }

    if (finalString === '') {
        return '-';
    }
    return finalString;
}
