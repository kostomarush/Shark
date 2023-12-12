/*
Template Name: Greeva - Responsive Bootstrap 4 Admin Dashboard
Author: CoderThemes
Version: 2.0.0
Website: https://coderthemes.com/
Contact: support@coderthemes.com
File: Datatables init js
*/

$(document).ready(function() {

    // Default Datatable
    $('#datatable').DataTable({
        "pageLength": 5,
        "searching": false,
        "lengthChange": false,
        "ordering": true,
        "info": true,
        "language": {
        "info": "Задачи с _START_ по _END_ из _TOTAL_",
        "paginate": {
            "first": "Первая",
            "last": "Последняя",
            "next": "Следующая",
            "previous": "Предыдущая"
        }
        }
        });
    
        $('#datatable_seg').DataTable({
            "pageLength": 5,
            "searching": false,
            "lengthChange": false,
            "ordering": true,
            "info": false,
            "language": {
            "paginate": {
                "first": "Первая",
                "last": "Последняя",
                "next": "Следующая",
                "previous": "Предыдущая"
            }
            }
            });

    //Buttons examples
    var table = $('#datatable-buttons').DataTable({
        lengthChange: false,
        buttons: ['copy', 'print']
    });

    // Multi Selection Datatable
    $('#selection-datatable').DataTable({
        "pageLength": 5,
        "searching": true,
        "lengthChange": true,
        "ordering": true,
        "info": true,
        "language": {
        "lengthMenu": "Показать _MENU_ записей на странице",
        "zeroRecords": "Ничего не найдено",
        "info": "Показаны записи с _START_ по _END_ из _TOTAL_",
        "infoEmpty": "Нет доступных записей",
        "infoFiltered": "(отфильтровано из _MAX_ записей)",
        "search": "Поиск:",
        "paginate": {
            "first": "Первая",
            "last": "Последняя",
            "next": "Следующая",
            "previous": "Предыдущая"
        }
        }

    });

    table.buttons().container()
            .appendTo('#datatable-buttons_wrapper .col-md-6:eq(0)');
} );

