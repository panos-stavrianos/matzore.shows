function monitor() {
    var socket = io();
    socket.on('connect', function () {
        socket.emit('monitor_autopilot', {data: 'I\'m connected!'});
    });
    socket.on('get_autopilot', result => {
        for (let song in result) {
            for (let key in result[song]) {
                $('#' + song + "_" + key).text(result[song][key])
            }
            $('#' + song + "_progress").attr('aria-valuenow', result[song]['Elapsed']);
            $('#' + song + "_progress").attr('aria-valuemax', result[song]['Duration']);
            $('#' + song + "_progress").width(result[song]['percent'] + '%')
        }
    });
}

monitor();

$(document).ready(() => {
    var now_date = new Date();
    var start_time = new Date(now_date.getFullYear(), now_date.getMonth(), now_date.getDate(), now_date.getHours()+1,0, 0);

    $('.timepicker').timepicker({
        timeFormat: 'HH:mm',
        interval: 60,
        minTime: '00:00',
        maxTime: '23:00',
        defaultTime: start_time,
        dynamic: true,
        dropdown: true,
        scrollbar: true,
        change: function (time) {
            // the input field
            var end_date = new Date(now_date.getFullYear(), now_date.getMonth(), now_date.getDate(), time.getHours(), time.getMinutes(), 0);
            if (now_date > end_date) {
                end_date = new Date(end_date.getTime() + (60 * 60 * 24 * 1000));
            }
            moment.locale('el');
            $('#until_help').text(moment(end_date).fromNow())

            // new Date((new Date()).getTime() + (60 * 60 * 24 * 1000));
            //
            // var seconds = (end_date.getTime() - now_date.getTime()) / 1000;
        }
    });


});
