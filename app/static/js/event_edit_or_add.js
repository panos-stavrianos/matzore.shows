$(document).ready(function () {

    let description = $('#description_editor').data("browse");

    description_editor = new tui.Editor({
        el: document.querySelector('#description_editor'),
        initialEditType: 'markdown',
        previewStyle: 'vertical',
        height: '500px',
        initialValue: description,
        hideModeSwitch: true
    });


    $("#event_form").submit(function (event) {
        $('#description_editor').html(`<textarea id="body" name="body" required="">${description_editor.getMarkdown()}</textarea>`);
        $('#event_date_container').html(`<input id="event_date" name="event_date" type="text" value="${$('#event_date').val()}">`);
    });

    $(".js-example-tags").select2({
        tags: true
    });

    $('.datetimepicker').datetimepicker({
        datepicker: {showOtherMonths: true},
        modal: true,
        footer: true,
        format: 'HH:MM dd/mm/yyyy',
    });

});