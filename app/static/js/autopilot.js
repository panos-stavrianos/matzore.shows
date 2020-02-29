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
            let progress = $('#' + song + "_progress")
            progress.attr('aria-valuenow', result[song]['Elapsed']);
            progress.attr('aria-valuemax', result[song]['Duration']);
            progress.width(result[song]['percent'] + '%')
        }
    });
}

monitor();

$(document).ready(() => {
    let now_date = new Date();
    let start_time = new Date(now_date.getFullYear(), now_date.getMonth(), now_date.getDate(), now_date.getHours() + 1, 0, 0);
    let start_time_string = moment(start_time).format("HH:mm");

    $('.timepicker').timepicker({
        modal: true,
        footer: true,
        mode: '24hr',
        timeFormat: 'HH:mm',
        value: start_time_string,
        change: function (e) {
            // the input field
            time = new Date(moment($('.timepicker').val(), 'HH:mm'));
            var end_date = new Date(now_date.getFullYear(), now_date.getMonth(), now_date.getDate(), time.getHours(), time.getMinutes(), 0);
            if (now_date > end_date)
                end_date = new Date(end_date.getTime() + (60 * 60 * 24 * 1000));

            moment.locale('el');
            $('#until_help').text(moment(end_date).fromNow())
        }
    });

});
