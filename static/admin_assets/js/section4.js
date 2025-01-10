$(document).ready(function () {

    $('#section4 input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });

    // On blur of IFSC fetching all bank data
    $('#ifsc_code').on('blur', function () {
        let ifsc = $(this).val()
        $.ajax({
            url: "/get_ifsc_data",
            type: "GET",
            data: { 'ifsc': ifsc },
            success: function (html) {
                if (html.error) {
                    Swal.fire({
                        title: "Wrong IFSC",
                        text: "Please Enter Correct IFSC",
                        icon: "info"
                    });
                } else {
                    $('#bank_name').val(html.BANK)
                    $('#micr').val(html.MICR)
                }
            },
            error: function (jqxhr, textStatus, error) {
                Swal.fire({
                    title: "Wrong IFSC",
                    text: "Please Enter Correct IFSC",
                    icon: "info"
                });
            }
        })

    })

    $('#work_in_government').on('change',function(){
        if($(this).val() == 'Yes'){
            $('#govern_id').removeClass('d-none')
        }else{
            $('#govern_id').addClass('d-none')
        }
    })
})