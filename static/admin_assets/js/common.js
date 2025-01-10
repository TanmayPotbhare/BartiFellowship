$(document).ready(function () {

    var currentRoute = window.location.pathname;
    var containsSection = currentRoute.indexOf('section') !== -1;
    // Display the result
    if (containsSection) {
        var lastItem = currentRoute[currentRoute.length - 1];
        for (i = 1; i <= lastItem; i++) {
            $('.bar-' + i).addClass('bar-active')
        }
    }
    $('.tooltip-trigger').tooltip();
    $('.tooltip').tooltip();
    $('#candidate_preview').hide()
    $('#caste_wrapper').hide()
    $('#identity_prev').hide()
    $('#add_prev').hide()
    $('#qual_prev').hide()
    $('#income_prev').hide()
    $('#domicile_prev').hide()
    $('#caste_prev').hide()
    $('#medical_prev').hide()
    $('#bank_prev').hide()
    $('#gov_prev').hide()
    $(document).on('change', '#candidate_photo', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#candidate_preview').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#candidate_preview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#candidate_preview').hide()
            $('#candidate_preview').attr('src', '');
        }


    })
    $(document).on('change', '#identity_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#identity_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#identity_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#identity_prev').hide()
            $('#identity_prev').attr('src', '');
        }


    })
    $(document).on('change', '#add_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#add_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#add_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#add_prev').hide()
            $('#add_prev').attr('src', '');
        }


    })
    $(document).on('change', '#qual_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#qual_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#qual_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#qual_prev').hide()
            $('#qual_prev').attr('src', '');
        }


    })
    $(document).on('change', '#income_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#income_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#income_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#income_prev').hide()
            $('#income_prev').attr('src', '');
        }


    })
    $(document).on('change', '#domicile_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#domicile_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#domicile_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#domicile_prev').hide()
            $('#domicile_prev').attr('src', '');
        }


    })
    $(document).on('change', '#medical_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#medical_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#medical_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#medical_prev').hide()
            $('#medical_prev').attr('src', '');
        }


    })
    $(document).on('change', '#Bank_Proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#bank_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#bank_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#bank_prev').hide()
            $('#bank_prev').attr('src', '');
        }


    })
    $(document).on('change', '#gov_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#gov_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#gov_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#gov_prev').hide()
            $('#gov_prev').attr('src', '');
        }


    })
    $(document).on('change', '#caste_proof', function () {
        var input = this;
        var url = $(this).val();
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (ext == "gif" || ext == "png" || ext == "jpeg" || ext == "jpg")) {
            $('#caste_prev').show()
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#caste_prev').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
        else {
            $('#caste_prev').hide()
            $('#caste_prev').attr('src', '');
        }


    })

    $('#caste_option').on('change', function () {
        if ($(this).val() == 'Yes') {
            $('#caste_wrapper').show()
        } else {
            $('#caste_wrapper').hide()
        }
    })
    $('#dob').on('blur', function () {

        // Get the user's date of birth from the input field
        var dob = new Date($("#dob").val());

        // Calculate the age
        var today = new Date();
        var age = today.getFullYear() - dob.getFullYear();
        // Check if the user hasn't had their birthday this year yet
        if (today.getMonth() < dob.getMonth() || (today.getMonth() === dob.getMonth() && today.getDate() < dob.getDate())) {
            age--;
        }

        // Display the result
        if (age > 45 || age < 18) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "We're sorry, but this Fellowship is only open to individuals aged 18 to 45. Thank you for your interest.",
                footer: '<a href="/">Sign Out</a>'
            })
        } else {
            $('#age').val(age).prop('readonly', true);
        }

    })
    $('#date_of_birth').on('blur', function () {

        // Get the user's date of birth from the input field
        var date_of_birth = new Date($("#date_of_birth").val());

        // Calculate the age
        var today = new Date();
        var age = today.getFullYear() - date_of_birth.getFullYear();
        // Check if the user hasn't had their birthday this year yet
        if (today.getMonth() < date_of_birth.getMonth() || (today.getMonth() === date_of_birth.getMonth() && today.getDate() < date_of_birth.getDate())) {
            age--;
        }

        // Display the result
        if (age > 45 || age < 21) {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: "Sorry, but we cannot accept individuals between the age of 21 to 45 for this Fellowship. Thank you for your interest.",
                footer: '<a href="/">Sign Out</a>'
            })
            $(this).val('')
            $('#age').val('')
        } else {
            $('#age').val(age).prop('readonly', true);
        }

    })
    $('#caste_option').on('change', function () {
        if ($('#caste_option').val() == 'Yes') {
            $('#issuing_district').attr('readonly', false)
            $('#caste_issuing_authority').attr('readonly', false)
            $('#caste_issuing_authority').attr('disabled', false)
            $('#issuing_district').attr('disabled', false)
            $('#caste_cert_number').attr('readonly', false)

        } else if ($('#caste_option').val() == 'No') {
            Swal.fire({
                icon: 'warning',
                title: 'Sorry',
                text: "Sorry, you cannot apply to this scheme Caste Certificate is mandatory",
                footer: '<a href="/">Sign Out</a>'
            })
            $(this).val('')
        }
        else {
            $('#issuing_district').attr('readonly', true)
            $('#caste_issuing_authority').attr('readonly', true)
            $('#caste_issuing_authority').attr('disabled', true)
            $('#issuing_district').attr('disabled', true)
            $(this).val('')
        }
    })

    // On change shows the college data on university identity
    $('#Board').on('change', function () {
        var value = $(this).val()
        $('#name_of_college').empty();

        $.ajax({
            url: '/get_college_by_university',
            method: 'POST',
            data: value,
            success: function (html) {
                $('#name_of_college').select2({
                    data: [
                        { id: '', text: '--SELECT COLLEGE--' },
                    ]

                });
                $('#name_of_college').select2({
                    placeholder: 'Select College',
                    data: html
                });

            }
        })
    })


    // File size validation and check file extension
    $('.file_validation').on('change', function () {
        // File extension allowed on site
        var allowExtensions = ['pdf', 'jpg', 'jpeg', 'png'];

        // Max file size is defined (2MB)
        var maxFileSize = 2 * 1024 * 1024;

        // Get selected file
        var uploadFile = this.files[0];

        if (uploadFile) {
            var fileName = uploadFile.name;
            var fileExtension = fileName.split('.').pop().toLowerCase();

            if (allowExtensions.indexOf(fileExtension) === -1) {
                Swal.fire({
                    icon: 'error',
                    title: 'Sorry',
                    text: 'Invalid file type. Allowed file types are PDF, JPG, JPEG, PNG.'
                });
                $(this).val('')
            }

            if (uploadFile.size > maxFileSize) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Sorry',
                    text: 'File size exceeds the maximum allowed size of 2MB.',
                });
                $(this).val('')
            }
        }

    })

    // Accept image format only for input type file 
    $('.accept_img').on('change', function () {
        // File extension allowed on site
        var allowExtensions = ['jpg', 'jpeg', 'png'];

        // Max file size is defined (2MB)
        var maxFileSize = 2 * 1024 * 1024;

        // Get selected file
        var uploadFile = this.files[0];

        if (uploadFile) {
            var fileName = uploadFile.name;
            var fileExtension = fileName.split('.').pop().toLowerCase();

            if (allowExtensions.indexOf(fileExtension) === -1) {
                Swal.fire({
                    icon: 'error',
                    title: 'Sorry',
                    text: 'Invalid file type. Allowed file types are JPG, JPEG, PNG.'
                });
                $(this).val('')
            }

            if (uploadFile.size > maxFileSize) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Sorry',
                    text: 'File size exceeds the maximum allowed size of 2MB.',
                });
                $(this).val('')
            }
        }

    })
    // Accept pdf format only for input type file 
    $('.accept_pdf').on('change', function () {
        // File extension allowed on site
        var allowExtensions = ['pdf'];

        // Max file size is defined (2MB)
        var maxFileSize = 2 * 1024 * 1024;

        // Get selected file
        var uploadFile = this.files[0];

        if (uploadFile) {
            var fileName = uploadFile.name;
            var fileExtension = fileName.split('.').pop().toLowerCase();

            if (allowExtensions.indexOf(fileExtension) === -1) {
                Swal.fire({
                    icon: 'error',
                    title: 'Sorry',
                    text: 'Invalid file type. Allowed file types are PDF.'
                });
                $(this).val('')
            }

            if (uploadFile.size > maxFileSize) {
                Swal.fire({
                    icon: 'warning',
                    title: 'Sorry',
                    text: 'File size exceeds the maximum allowed size of 2MB.',
                });
                $(this).val('')
            }
        }

    })

    // Medical disability
    $('#disability').on('change', function () {
        if ($(this).val() == 'Yes') {
            $('#medical_proof').attr('readonly', false)
            $('#medical_proof').attr('disabled', false)
            $('#medical_proof').attr('required', true)
        } else {
            $('#medical_proof').attr('readonly', true)
            $('#medical_proof').attr('disabled', true)
            $('#medical_proof').attr('required', false)
            $('#medical_proof').val('')
        }
    })

    // GOvernment
    $('#work_in_government').on('change', function () {
        if ($(this).val() == 'Yes') {
            $('#gov_proof').attr('readonly', false)
            $('#gov_proof').attr('disabled', false)
            $('#gov_proof').attr('required', true)
        } else {
            $('#gov_proof').attr('readonly', true)
            $('#gov_proof').attr('disabled', true)
            $('#gov_proof').attr('required', false)
            $('#gov_proof').val('')
            $('#gov_prev').attr('src', '')
            $('#gov_prev').hide()
        }
    })

    // My new code Starts here

    // ########## Pagination code starts here #########
    // go to page two
    $('.next-btn-2').on('click', function () {
        $('.page-1').hide()
        $('.page-2').fadeIn()
        $('.bar-2').addClass('bar-active')
    })
    $('.next-btn-3').on('click', function () {
        $('.page-2').hide()
        $('.page-3').fadeIn()
        $('.bar-3').fadeIn('slow', 2000).addClass('bar-active')
    })
    // Previous to page 1
    $('.preview-btn-1').on('click', function () {
        $('.page-2').hide()
        $('.page-1').fadeIn()
        $('.bar-2').removeClass('bar-active')
    })
    $('.preview-btn-2').on('click', function () {
        $('.page-3').hide()
        $('.page-2').fadeIn()
        $('.bar-3').removeClass('bar-active')
    })

    $('.preview-btn-2').on('click', function () {
        $('.page-3').hide()
        $('.page-2').fadeIn()
        $('.bar-3').removeClass('bar-active')
    })
    $('.preview-btn-3').on('click', function () {
        $('.page-4').hide()
        $('.page-3').fadeIn()
        $('.bar-4').removeClass('bar-active')
    })
    $('.next-btn-4').on('click', function () {
        $('.page-3').hide()
        $('.page-4').fadeIn()
        $('.bar-4').addClass('bar-active')
    })
    $('.next-btn-5').on('click', function () {
        $('.page-4').hide()
        $('.page-5').fadeIn()
        $('.bar-5').addClass('bar-active')
    })
    $('.preview-btn-4').on('click', function () {
        $('.page-5').hide()
        $('.page-4').fadeIn()
        $('.bar-5').removeClass('bar-active')
    })

    // ############## Pagination code  Ends Here ##########
    // Adhar card validation
    $('#aadhaar').on('blur', function () {
        let adhar_no = $(this).val()
        if (adhar_no[0] == 0) {
            Swal.fire({
                title: "Please Check",
                text: "Please Enter Correct Adhar Number",
                icon: "info"
            });
            $(this).val('')
        }
        if (adhar_no.length < 12) {
            Swal.fire({
                title: "Please Check",
                text: "Number should be 12 digits ",
                icon: "info"
            });

        }
    })

    // Preview Form edit view
    $('.edit_preview_btn').on('click', function () {
        var id = $(this).attr('data-hidden')
        $('#' + id).prop('disabled', function (_, value) {
            return !value;
        });
    })
    $('.edit_alert').on('click', function () {
        Swal.fire({
            title: "You Can't Edit this Field",
            text: '',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    })
    $('#submit_preview').on('click', function (e) {
        $('#preview_form').validate({
            errorClass: 'text-danger', // Custom class for error messages
            errorElement: 'div',
            errorPlacement: function (error, element) { // Customize the placement of error messages
                // Append error message to the parent element
                // error.appendTo(element.parent());

                // Update placeholder text to include error message
                var placeholderText = element.attr('placeholder');
                element.attr('placeholder', placeholderText + ' - ' + error.text()).addClass('pl-red');
            }
        })
        e.preventDefault()
        $('.disabled_class').attr('disabled', false)
        Swal.fire({
            title: "Do you want to submit?",
            text: "After submitting the form, please note that you won't be able to update any information. Kindly review your entries before submission to ensure accuracy",
            icon: 'warning',
            showDenyButton: false,
            showCancelButton: true,
            confirmButtonText: "Submit",
        }).then((result) => {
            /* Read more about isConfirmed, isDenied below */
            if (result.isConfirmed) {
                $('#preview_form').submit()
            } else {
                Swal.fire("Please check your form Again", "", "info");
            }
        });



    })

    $('#preview_form .text-capitalize').on('change blur', function () {
        let text = $(this).val()
        $(this).val(capitalizeText(text))
    })
    function capitalizeText(text) {
        return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    }

    $('#preview_form .accept_english').on('change', function () {
        if (/[^a-zA-Z\s,/]/.test(this.value)) {
            this.value = this.value.replace(/[^a-zA-Z,\s/0-9]/g, '');
            Swal.fire({
                title: "Please Check",
                text: "Only English Text Accept",
                icon: "info"
            });

        }
    })
    $('#preview_form #adhaar_number').on('blur', function () {
        let adhar_no = $(this).val()
        if (adhar_no[0] == 0) {
            Swal.fire({
                title: "Please Check",
                text: "Please Enter Correct Adhar Number",
                icon: "info"
            });
            $(this).val('')
        }
        if (adhar_no.length < 12) {
            Swal.fire({
                title: "Please Check",
                text: "Number should be 12 digits ",
                icon: "info"
            });

        }
    })
    $('#preview_form #mobile_number').on('blur', function () {
        let adhar_no = $(this).val()
        if (adhar_no[0] < 6) {
            Swal.fire({
                title: "Please Check",
                text: "Please Enter Correct Mobile Number",
                icon: "info"
            });
            $(this).val('')
        }
        if (adhar_no.length < 10) {
            Swal.fire({
                title: "Please Check",
                text: "Number should be 10 digits ",
                icon: "info"
            });

        }
    })

    $('#preview_form #pincode').on('blur', function () {
        $('#preview_form #village').empty()
        $('#preview_form #village').append(`<option value = '' class = 'spinner-border' role="status"> 
        <span class="sr-only">Loading...</span> </option>`)
        let pincode = $(this).val();
        if ($(this).val() == '' || $(this).val().length < 6) {
            Swal.fire({
                title: "Wrong Pincode",
                text: "Please Enter 6 digits Pincode",
                icon: "info"
            });
            return
        }
        if (pincode[0] == 0) {
            Swal.fire({
                title: "Wrong Pincode",
                text: "Enter Correct piconde",
                icon: "info"
            });
            $(this).val('')
            return
        }

        $.ajax({
            url: "/get_pincode_data",
            type: "GET",
            data: { 'pincode': pincode },
            success: function (html) {
                $('#preview_form #village').empty()
                if (html.Message == 'No records found') {
                    Swal.fire({
                        title: "Wrong Pincode",
                        text: "Please Enter Correct Pincode",
                        icon: "info"
                    });
                } else {

                    let PostOffice = html.result
                    $('#preview_form #village').append(`<option value = ''> -- Select Village -- </option>`)
                    $(PostOffice).each(function (index, post_val) {
                        $('#preview_form #village').append(`<option value = '${post_val.id}'>${post_val.postalLocation}</option>`)
                    })
                }
            },
            error: function (jqxhr, textStatus, error) {
            }
        });
    });

    // Get Pincode and village and show the other details on preview page
    $('#preview_form #village').on('change', function () {
        village_name = $(this).val();
        pincode = $('#preview_form #pincode').val()
        $.ajax({
            url: "/get_pincode_data",
            type: "GET",
            data: { 'pincode': pincode },
            success: function (html) {
                if (html.Message == 'No records found') {
                    Swal.fire({
                        title: "Wrong Pincode",
                        text: "Please Enter Correct Pincode",
                        icon: "info"
                    });
                } else {

                    let PostOffice = html.result
                    $(PostOffice).each(function (index, post_val) {
                        if (post_val.id == village_name) {
                            $('#preview_form #taluka').val(post_val.province)
                            $('#preview_form #city').val(post_val.district)
                            $('#preview_form #district').val(post_val.district)
                            $('#preview_form #state').val(post_val.state)
                        }
                    })
                }
            },
            error: function (jqxhr, textStatus, error) {
            }
        })
    })

$('.select2').select2();

})

$('#phd_thesis').on('change', function () {

    url = $(this).val()
    ext = url.split('.')
    if (ext[1].toLowerCase() != 'pdf') {
        Swal.fire({
            icon: "error",
            title: "Please Try Agian...",
            text: `Invalid File Type. Sorry only PDF file accepted`,
        });
    }
})

$('#select_fy_year').on('change', function () {
    year = $('#select_fy_year :selected').text()
    $.ajax({
        url:''
    })
    $('h3 .selected_year').html(year)
})
//let inputs = $('#preview_form input')
//inputs.each(function () {
//    let inputval = $(this).val()
//    if (inputval.toLowerCase() == 'none' || inputval == '' && $(this).attr('type') != 'file') {
//        $(this).val('')
//    }
//})