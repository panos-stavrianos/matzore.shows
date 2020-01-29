function get_actions_html(id, name) {
    return `<a href="member/${id}" title="Προβολή">  <i class="fas fa-eye text-success"></i></a>
     <a href="member_edit/${id}" title="Επεξεργασία">  <i class="fas fa-edit text-warning"></i></a>
     <a href="member_delete/${id}" title="Διαγραφή μέλους" class="delete" onclick="return confirm('Σίγουρα θέλετε να διαγράψετε το μέλος ${name}')"> 
            <i class="fas fa-trash-alt text-danger"></i>
     </a>
`
}

$(document).ready(function () {
    var members_table = $('#members_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": "/get_members",
        "order": [[1, "asc"]],

        columns: [
            {data: "id", visible: false},
            {
                data: "name",
                render: function (data, type, row, meta) {
                    return `<a href="member/${row.id}">${row.name}</a>`;
                }
            },
            {
                data: "email",
                render: function (data, type, row, meta) {
                    return `<a href="member/${row.id}">${row.email}</a>`;
                }
            },
            {
                data: "phone",
                orderable: false,
            },
            {
                data: "facebook",
                orderable: false,
                render: function (data, type, row, meta) {
                    if (data === "")
                        return '<i class="fab fa-facebook text-dark"></i>';
                    return '<a href="' + data + '"> <i class="fab fa-facebook "></i></a>';
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



