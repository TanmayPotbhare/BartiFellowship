$(document).ready(function () {
    $('.select-all').on('click', function () {
        $(".email-input").each(function () {
            if ($('.select-all').prop('checked')) {
                $(this).prop('checked', true);
                $('.email-list').append(` <input type="hidden" name = "email_list[]" value = "${$(this).val()}"> `)

            } else {
                $(this).prop('checked', false);
                $('.email-list').empty()
            }
        });
    });

    $('.email-input').on('click', function () {
        if ($(this).prop('checked')) {
            $(this).prop('checked', true);
            $('.email-list').append(` <input type="hidden" name = "email_list[]" value = "${$(this).val()}"> `)

        } else {
            $('.email-list').find(`input[value='${$(this).val()}']`).remove();
        }
    })

    $('#mail_type').on('change', function () {
        if ($(this).val() == 'bulk') {
            $('#search_option').removeClass('d-none')
            $('#bulk_section').removeClass('d-none')
            $('#custom_section').addClass('d-none')
        } else if($(this).val() == 'custom'){
            $('#search_option').addClass('d-none')
            $('#bulk_section').addClass('d-none')
            $('#custom_section').removeClass('d-none')
        }
    })



    // For Custom Email Section
    // Add Email input on click of plus button 
    $('#add_email_input').on('click', function () {
        $('#custom_email_wrapper').append(`
        <div class="col-md-3">
            <label for="">Enter Email</label>
            <div class="input-group mb-3">
                <input type="text" class="form-control custom_email" placeholder="Enter Email" aria-label="Enter Email" aria-describedby="button-addon2">
                <button class="btn btn-theme remove_email_input" type="button" id="button-addon2"><i class = 'ri-close-fill'></i></button>
            </div>
        </div>
        
        `)
    })


});

$(document).on('click', '.remove_email_input', function () {
    $(this).closest('.col-md-3').remove();
    $('.email-list').find(`input[value='${$(this).parent().find('.custom_email').val()}']`).remove();
})
$(document).on('blur', '.custom_email', function () {
    if ($(this).val() != '') {
        var email = $(this).val();
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (emailRegex.test(email)) {
            $('.email-list').append(` <input type="hidden" name = "email_list[]" value = "${$(this).val()}"> `)
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Wrong E-mail',
                text: "Please Enter correct email.",
            })
        }
    }


    
    // 
})