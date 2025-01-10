$(document).ready(function () {
    $('#months').on('change', function () {
        fellowship_amt = parseFloat($('#fellowship').val())
        months = parseFloat($('#months').val())
        rate_of_int = parseFloat($('#rate').val());
        rate_amt = (fellowship_amt * rate_of_int / 12) / 100 * months
        total_amt = fellowship_amt + rate_amt
        $('#amount').val(rate_amt.toFixed(2))
        $('#total_hra').val(total_amt.toFixed(2))
    })
})