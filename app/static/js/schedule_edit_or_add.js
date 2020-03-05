$(document).ready(() => {
    $('#from_time').timepicker({
        modal: true,
        footer: true,
        mode: '24hr',
        timeFormat: 'HH:mm',
        value: $('#from_time').data().value
    });
    $('#to_time').timepicker({
        modal: true,
        footer: true,
        mode: '24hr',
        timeFormat: 'HH:mm',
        value: $('#to_time').data().value,
    });
});