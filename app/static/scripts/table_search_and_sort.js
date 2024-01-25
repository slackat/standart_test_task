document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchForm').addEventListener('submit', function (e) {
        e.preventDefault();
        let formData = new FormData(this);
        fetch('/get_requisites?' + new URLSearchParams(formData).toString())
            .then(response => response.json())
            .then(data => updateTable(data))
            .catch(error => console.error('Error:', error));
    });

    document.querySelectorAll('.sort-link').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            let column_to_sort = this.dataset.sort;
            let order_by = 'asc';
            if (this.classList.contains('desc')) {
                order_by = 'asc';
                this.classList.remove('desc');
            } else {
                order_by = 'desc';
                this.classList.add('desc');
            }
            let formData = new FormData(document.getElementById('searchForm'));
            formData.append('sort', column_to_sort);
            formData.append('order', order_by);
            fetch('/get_requisites?' + new URLSearchParams(formData).toString())
                .then(response => response.json())
                .then(data => updateTable(data))
                .catch(error => console.error('Error:', error));
        });
    });

    function updateTable(data) {
        const requisitesTable = document.getElementById('requisitesTable');
        const tbody = requisitesTable.querySelector('tbody');
        tbody.innerHTML = '';
        data.forEach(requisite => {
            const row = '<tr>' +
                '<td>' + requisite.id + '</td>' +
                '<td>' + requisite.payment_type + '</td>' +
                '<td>' + requisite.account_type + '</td>' +
                '<td>' + requisite.owner_name + '</td>' +
                '<td>' + requisite.phone_number + '</td>' +
                '<td>' + requisite.value_limit + '</td>' +
                '</tr>';
            tbody.insertAdjacentHTML('beforeend', row);
        });
    }
});
