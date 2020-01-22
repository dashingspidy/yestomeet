 $(function () {
    var start = new Date();
    start.setFullYear(start.getFullYear() - 99);
    var end = new Date();
    end.setFullYear(end.getFullYear() - 18);

    $('#birthdate').datepicker({
        dateFormat: 'dd/mm/yy',
        changeMonth: true,
        changeYear: true,
        minDate: start,
        maxDate: end,
        yearRange: start.getFullYear() + ':' + end.getFullYear()
    });
    $('#birthdate').on('change', function()  {
        var date = Date.parse($(this).val());
        if (date > end) {
            $('#berror').show();
            $(this).val('');
        }
    });
});