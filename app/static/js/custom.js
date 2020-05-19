$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
String.prototype.remove_timezone = function () {
    return this.replace(this.substr(this.indexOf('GMT')), '')
};
String.prototype.hash = function () {
    var self = this, range = Array(this.length);
    for (var i = 0; i < this.length; i++) {
        range[i] = i;
    }
    return Array.prototype.map.call(range, function (i) {
        return self.charCodeAt(i).toString(16);
    }).join('');
};

function show_sidebar(val) {
    if (val) {//to show
        $('#accSidebar').removeClass('d-none');
    } else {//to remove
        $('#accSidebar').addClass('d-none');
    }
}

$(document).ready(() => {
    var lastWidth = $(window).width();
// Close any open menu accordions when window is resized below 768px
    if ($(window).width() < 576)
        show_sidebar(false);
    else
        show_sidebar(true);

    $(window).resize(function () {
        if ($(window).width() !== lastWidth) {
            lastWidth = $(window).width();
            if ($(window).width() < 576)
                show_sidebar(false);
            else
                show_sidebar(true);
        }
    });

    $('#sidebarOpen').click(function () {
        show_sidebar(true);
    });

    $('#sidebarClose').on('click', function () {
        show_sidebar(false);
    });
    $('.toggle').css({
        "min-width": "70px",
    });


    $(document).on("change", ".uploadFile", function () {
        var uploadFile = $(this);
        var files = !!this.files ? this.files : [];
        if (!files.length || !window.FileReader) return; // no file selected, or no FileReader support

        if (/^image/.test(files[0].type)) { // only image file
            var reader = new FileReader(); // instance of the FileReader
            reader.readAsDataURL(files[0]); // read the local file

            reader.onloadend = function () { // set image data as background of div
                //alert(uploadFile.closest(".upimage").find('.imagePreview').length);
                // uploadFile.closest(".imgUp").find('.imagePreview').s("src", "url(" + this.result + ")");
                uploadFile.closest(".imgUp").find('.imagePreview').attr('src', this.result);
            }
        }

    });

});


