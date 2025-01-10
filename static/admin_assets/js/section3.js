$(document).ready(function () {

     $('#section3 input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });

    $('#validity_certificate').on('change', function () {
        let choice = $(this).val()
        if (choice == 'No') {
            Swal.fire({
                title: "Sorry",
                text: "Sorry, you cannot apply to this scheme, Caste Validity Certificate is mandatory",
                icon: "error"
            });
            $(this).val('')
        }else{
            $('#validity_num').attr('readonly',false)
            $('#validity_issuing_district').attr('readonly',false)
            $('#validity_issuing_authority').attr('readonly',false)
        }
    })

    // Disability 

    $('#disability').on('change',function(){
        if($(this).val() == 'Yes'){
            $('#typeDisabilityContainer').removeClass('d-none')
        }
        else if($(this).val() == 'No'){
            $('#typeDisabilityContainer').addClass('d-none')
        }
    })


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

    $('#domocile').on('change', function () {
        if($(this).val() == 'Yes'){
            $('#domocile_certificate').attr('disabled',false)
            $('#domocile_number').attr('readonly',false)
        }else if($(this).val() == 'No'){
            Swal.fire({
                    title: "Sorry",
                    text: "Sorry, you cannot apply to this scheme, Domicile Certificate is mandatory",
                    icon: "error"
                });
             $('#domocile_certificate').attr('disabled',true)
            $('#domocile_number').attr('readonly',true)
        }
    })



})