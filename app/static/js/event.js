$(document).ready(function () {
    let description = $('#description').data("browse");
    tui.Editor.factory({
        el: document.querySelector('#description'),
        viewer: true,
        height: '500px',
        initialValue: description
    });


});


var map;


function initMap() {
    // The location of Uluru

    var uluru = {lat: -25.344, lng: 131.036};
    // The map, centered at Uluru
    map = new google.maps.Map(
        document.getElementById('map'), {zoom: 4, center: uluru});
    // The marker, positioned at Uluru
    var marker = new google.maps.Marker({position: uluru, map: map});
}