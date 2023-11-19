document.addEventListener('DOMContentLoaded', function() {
    var Min = 200 * 1000;
    var Max = 300 * 1000;
    Delay = Math.random() * (Max - Min) + Min;
    setTimeout(function() {
        var Modal = new bootstrap.Modal(document.getElementById('viTimerModal'));
        Modal.show();
    }, Delay);
});
