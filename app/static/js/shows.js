function get_actions_html(id, name) {
    return `<a href="show/${id}" title="Προβολή">  <i class="fas fa-eye text-success"></i></a>
     <a href="show_edit/${id}" title="Επεξεργασία">  <i class="fas fa-edit text-warning"></i></a>
     <a href="show_delete/${id}" title="Διαγραφή εκπομπής" class="delete" onclick="return confirm('Σίγουρα θέλετε να διαγράψετε την εκπομπή ${name}')"> 
            <i class="fas fa-trash-alt text-danger"></i>
     </a>
`
}

function get_social_html(name, value) {
    let color = value === "" ? 'text-dark' : '';
    return `<a href="${value}">  <i class="fab fa-${name} ${color}"></i></a>`
}

function get_socials_html(row) {
    return `${get_social_html('facebook', row.facebook)}
     ${get_social_html('instagram', row.instagram)} 
     ${get_social_html('twitter', row.twitter)}`
}

$(document).ready(function () {
    var shows_table = $('#shows_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": "/get_shows",
        "order": [[1, "asc"]],
        columns: [
            {data: "id", visible: false},
            {
                data: "name",
                render: function (data, type, row, meta) {
                    return `<a href="show/${row.id}">${row.name}</a>`;
                }
            },
            {
                data: "description",
                render: function (data, type, row) {
                    return `<a href="show/${row.id}">${data.substr(0, 50)}</a>`;
                }
            },
            {data: "email"},
            {
                orderable: false,
                render: function (data, type, row, meta) {
                    return get_socials_html(row);
                }
            },
            {
                orderable: false,
                render: function (data, type, row, meta) {
                    return get_actions_html(row.id, row.name);
                }
            }
        ]
    });

});
