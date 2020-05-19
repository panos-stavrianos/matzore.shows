$(document).ready(function () {
    let description = $('#description').data("browse");
    tui.Editor.factory({
        el: document.querySelector('#description'),
        viewer: true,
        height: '500px',
        initialValue: description
    });
});
