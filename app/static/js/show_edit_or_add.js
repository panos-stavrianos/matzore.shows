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


    $("#show_form").submit(function (event) {
        $('#description_editor').html(`<textarea id="description" name="description" required="">${description_editor.getMarkdown()}</textarea>`);
    });

});