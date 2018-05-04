var TextTransmitter = (function() {
    var button;
    var textbox;
    var warningbox;

    function onTransmitFinish(e) {
        e.target.disabled = false;
        console.log('finished');
    };

    function onClick(e) {
        var ssid = document.getElementById('ssid').value;
        var password = document.getElementById('password').value;
        var payload = String.fromCharCode(ssid.length) + ssid + password;
        if (ssid) {
            e.target.disabled = true;

            var profilename = 'ultrasonic-experimental';
            var onFinish = function() { return onTransmitFinish(e); };
            var transmit = Quiet.transmitter({profile: profilename, onFinish: onFinish, clampFrame: false});
            transmit.transmit(Quiet.str2ab(payload));
        }
        console.log(payload);
    };

    function onQuietReady() {
        var btn = document.getElementById('send');
        btn.addEventListener('click', onClick, false);
    };

    function onQuietFail(reason) {
        console.log("quiet failed to initialize: " + reason);
    };

    function onDOMLoad() {
        Quiet.addReadyCallback(onQuietReady, onQuietFail);
    };

    document.addEventListener("DOMContentLoaded", onDOMLoad);
})();
