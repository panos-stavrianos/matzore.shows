function monitor() {
    var socket = io();
    socket.on('connect', function () {
        socket.emit('monitor_autopilot', {data: 'I\'m connected!'});
    });
    socket.on('get_autopilot', result => {
        for (let song in result) {
            for (let key in result[song]) {
                console.log('#' + song + "_" + key + "------->" + result[song][key]);
                $('#' + song + "_" + key).text(result[song][key])
            }
            $('#' + song + "_progress").attr('aria-valuenow', result[song]['Elapsed']);
            $('#' + song + "_progress").attr('aria-valuemax', result[song]['Duration']);
            $('#' + song + "_progress").width(result[song]['percent'] + '%')
        }
    });
}

monitor();
