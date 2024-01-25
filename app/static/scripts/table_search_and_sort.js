$(document).ready(function () {
    $('#searchForm').submit(function (e) {
        e.preventDefault();
        let formData = $(this).serialize();
        $.ajax({
            type: 'GET',
            url: '/get_requisites',
            data: formData,
            dataType: 'json',
            success: function (data) {
                updateTable(data);
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });

    $('.sort-link').click(function (e) {
        e.preventDefault();
        let column_to_sort = $(this).data('sort');
        let order_by = 'asc';
        if ($(this).hasClass('desc')) {
            order_by = 'asc';
            $(this).removeClass('desc');
        } else {
            order_by = 'desc';
            $(this).addClass('desc');
        }
        $.ajax({
            type: 'GET',
            url: '/get_requisites',
            data: {
                sort: column_to_sort,
                order: order_by,
                search: $('#search').val(),
                search_field: $('#search_field').val()
            },
            dataType: 'json',
            success: function (data) {
                updateTable(data);
            },
            error: function (xhr, status, error) {
                console.error(error);
            }
        });
    });

    function updateTable(data) {
        $('#requisitesTable tbody').empty();
        $.each(data, function (index, requisite) {
            $('#requisitesTable tbody').append('<tr>' +
                '<td>' + requisite.id + '</td>' +
                '<td>' + requisite.payment_type + '</td>' +
                '<td>' + requisite.account_type + '</td>' +
                '<td>' + requisite.owner_name + '</td>' +
                '<td>' + requisite.phone_number + '</td>' +
                '<td>' + requisite.value_limit + '</td>' +
                '</tr>');
        });
    }
});