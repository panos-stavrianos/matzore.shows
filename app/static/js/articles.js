function get_actions_html(id, name) {
    return `<a href="article/${id}" title="Προβολή">  <i class="fas fa-eye text-success"></i></a>
     <a href="article_edit/${id}" title="Επεξεργασία">  <i class="fas fa-edit text-warning"></i></a>
     <a href="article_delete/${id}" title="Διαγραφή άρθρου" class="delete" onclick="return confirm('Σίγουρα θέλετε να διαγράψετε το άρθρο ${name}')"> 
            <i class="fas fa-trash-alt text-danger"></i>
     </a>
`
}


$(document).ready(function () {
    var articles_table = $('#articles_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": "/get_articles",
        "order": [[4, "desc"]],
        columns: [
            {data: "id", visible: false},
            {
                data: "title",
                render: function (data, type, row, meta) {
                    return `<a href="article/${row.id}">${row.title}</a>`;
                }
            },
            {
                data: "short_description",
                render: function (data, type, row) {
                    return `<a href="article/${row.id}">${data ? data.substr(0, 20) : ""}</a>`;
                }
            },
            {
                data: "published",
                render: function (data, type, row, meta) {
                    if (data)
                        return `<span class="badge badge-success"><i class="far fa-check-circle"></i></span>`;
                    else
                        return `<span class="badge badge-danger"><i class="far fa-times-circle"></i></span>`;
                }
            },
            {
                data: "created_at",
                render: function (data, type, row, meta) {
                    return moment(new Date(data)).format('DD/MM/YYYY HH:mm');
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
