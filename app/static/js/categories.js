function get_actions_html(id, name) {
    return `<a href="category/${id}" title="Προβολή">  <i class="fas fa-eye text-success"></i></a>
     <a href="category_edit/${id}" title="Επεξεργασία">  <i class="fas fa-edit text-warning"></i></a>
     <a href="category_delete/${id}" title="Διαγραφή κατηγορίας" class="delete" onclick="return confirm('Σίγουρα θέλετε να διαγράψετε την κατηγορία ${name}')"> 
            <i class="fas fa-trash-alt text-danger"></i>
     </a>`
}


$(document).ready(function () {
    var categories_table = $('#categories_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": "/get_categories",
        "order": [[1, "asc"]],
        columns: [
            {data: "id", visible: false},
            {
                data: "name",
                render: function (data, type, row, meta) {
                    return `<a href="category/${row.id}">${row.name}</a>`;
                }
            },
            {
                orderable: false,
                render: function (data, type, row, meta) {
                    return get_actions_html(row.id, row.title);
                }
            }
        ]
    });

});
