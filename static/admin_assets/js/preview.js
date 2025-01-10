
$(document).ready(function () {
    $('#preview_form input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });


    // SSC Passing year validation on preview page
    $('#preview_form #ssc_passing_year').on('blur', function () {
        let ssc_passing_yr = $(this).val();
        const d = new Date();
        let curr_year = d.getFullYear();
        let gap_yr = curr_year - ssc_passing_yr
        if (curr_year == ssc_passing_yr || ssc_passing_yr > curr_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. Please Enter correct passing year`,
            });
            $(this).val('')
        }
    })

    // Percentage validation
    $('#preview_form .percentage_validate').on('blur', function () {
        var inputValue = $(this).val();

        // Remove non-numeric and non-dot characters
        inputValue = inputValue.replace(/[^0-9.]/g, '');

        // Ensure the value is a valid number
        if ($.isNumeric(inputValue)) {
            // Convert the string to a floating-point number
            var percentage = parseFloat(inputValue);

            // Ensure the value is between 0 and 100
            if (percentage >= 0 && percentage <= 100) {
                // Round to two decimal places and update the input value
                if (percentage < 35) {
                    Swal.fire({
                        icon: "error",
                        title: "Sorry !....",
                        text: `Below 35 not accepted `,

                    });
                    $(this).val('');
                    return
                }
                $(this).val(percentage.toFixed(2));
            } else {
                // If not within the valid range, reset the input value
                $(this).val('');
                Swal.fire({
                    icon: "info",
                    title: "Please Try Again ....",
                    text: `Please enter a percentage between 0 and 100.`,

                });
            }
        } else {
            // If not a valid number, reset the input value
            $(this).val('');
            Swal.fire({
                icon: "info",
                title: "Please Try Again ....",
                text: `Please enter a valid percentage. `,

            });
        }
    });



    // HSC passing year validation
    $('#preview_form #hsc_passing_year').on('blur', function () {
        let hsc_passign_year = $(this).val();
        let ssc_passing_yr = $('#preview_form #ssc_passing_year').val()
        const d = new Date();
        let curr_year = d.getFullYear();
        let gap_yr = curr_year - hsc_passign_year
        if (ssc_passing_yr == hsc_passign_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. SSC and HSC passing year can't be same`,
            });
            $(this).val('')
            return
        }
        if (hsc_passign_year == curr_year || hsc_passign_year > curr_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. Please Enter correct passign year`,
            });
            $(this).val('')
            return
        }

    })

    // HSC passing year validation
    $('#preview_form #graduation_passing_year').on('blur', function () {
        let graduation_passing_year = $(this).val();
        let ssc_passing_yr = $('#preview_form #ssc_passing_year').val()
        let hsc_passing_year = $('#preview_form #hsc_passing_year').val()
        const d = new Date();
        let curr_year = d.getFullYear();
        let gap_yr = curr_year - graduation_passing_year
        if (ssc_passing_yr == graduation_passing_year || graduation_passing_year == hsc_passing_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. Graduation passing year can't same as per other passing year`,
            });
            $(this).val('')
            return
        }
        if (graduation_passing_year > curr_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. Please check the Graduation Year`,
            });
            $(this).val('')
            return
        }

    })

    // Post graduation year validation 
    $('#preview_form #phd_passing_year').on('blur', function () {
        let phd_passing_year = $(this).val()
        let graduation_passing_year = $('#preview_form #graduation_passing_year').val();
        let ssc_passing_yr = $('#preview_form #ssc_passing_year').val()
        let hsc_passing_year = $('#preview_form #hsc_passing_year').val()
        const d = new Date();
        let curr_year = d.getFullYear();
        let gap_yr = curr_year - phd_passing_year
        if (ssc_passing_yr == phd_passing_year || phd_passing_year == hsc_passing_year || phd_passing_year == graduation_passing_year || phd_passing_year > curr_year) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `Invalid Passing year. Please check the Post Graduation Year`,
            });
            $(this).val('')
            return
        }
    })


    // PHD registration date and phd registration  year validation
//    $('#preview_form #phd_registration_date').on('blur', function () {
//        let phd_registration_date = $(this).val()
//        let phd_registration_year = $('#phd_registration_year').val()
//        let d = new Date(phd_registration_date)
//        let year = d.getFullYear()
//        if (phd_registration_year != year) {
//            Swal.fire({
//                icon: "error",
//                title: "Please Try Agian...",
//                text: `Invalid Registration Date. The registration date's year does not match the registration year.`,
//            });
//            $(this).val('')
//        }
//
//    })

      $('#preview_form #phd_registration_date').on('blur', function () {
            let phd_registration_date = $(this).val();
            let phd_registration_year = $('#phd_registration_year').val();
            let d = new Date(phd_registration_date);
            let year = d.getFullYear();
            let month = d.getMonth(); // Get the month (0-11)

            // Define the range: April of registration year to March of the following year
            let startDate = new Date(phd_registration_year, 3, 1); // April 1st of registration year
            let endDate = new Date(parseInt(phd_registration_year) + 1, 2, 31); // March 31st of the following year

            // Check if the entered date is within the specified range
            if (d >= startDate && d <= endDate) {
                // Date is within the range, no action needed
                console.log("Valid registration date.");
            } else {
                // Date is outside the range, show an error message
                Swal.fire({
                    icon: "error",
                    title: "Invalid Registration Date",
                    text: `The registration date must be between April ${phd_registration_year} and March ${parseInt(phd_registration_year) + 1}.`,
                });
                // Clear the value of the registration date input field
                $(this).val('');
            }
        })

    $('#preview_form #family_annual_income').on('blur', function () {
        family_annual_income = $(this).val()
        if (parseInt(family_annual_income) > 800000) {
            Swal.fire({
                icon: "error",
                title: "Please Try Agian...",
                text: `More Than 8 lakhs income not accepted.`,
            });
            $(this).val('')
        }
    })

    // On blur of IFSC fetching all bank data
    $('#preview_form #ifsc_code').on('blur', function () {
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

    // Get College details by university
    $('#concerned_university').on('change', function () {
        let university_id = $('option:selected', this).attr('data-hidden')
        $('#selected_college').empty()
        $('#selected_college').append('<option>Loading ....</option>')
        $.ajax({
            url: '/get_college_data_by_university',
            method: 'POST',
            data: { 'u_id': university_id },
            success: function (html) {
                $('#selected_college').empty()
                $('#selected_college').append('<option>-- Select College --</option>')
                html.forEach(function (item) {

                    $('#selected_college').append(`<option value="${item.college_name}">${item.college_name}</option`);

                });
            },
            error: function () {
                Swal.fire({
                    icon: "error",
                    title: "Please Try Agian...",
                    text: `Please Select Correct University`,
                });
            }
        })
    })

    $('#validity_certificate').on('change', function () {
        if ($('#validity_certificate').val() == 'No'){
            Swal.fire({
                icon: 'warning',
                title: 'Sorry',
                text: "Sorry, you cannot apply to this 'SCHEME' -- Validity Certificate is mandatory",
                footer: '<a href="/">Sign Out</a>'
            })
        }
    })

    $('#caste_certf').on('change', function () {
        if ($('#caste_certf').val() == 'No'){
            Swal.fire({
                icon: 'warning',
                title: 'Sorry',
                text: "Sorry, you cannot apply to this 'SCHEME' -- Caste Certificate is mandatory",
                footer: '<a href="/">Sign Out</a>'
            })
        }
    })

    $('.only_text_allowed').on('change', function () {
        var inputValue = $(this).val();

        // Regular expression to match only alphabetic characters
        var regex = /^[a-zA-Z\s]+$/;

        // Test if the input value contains only text
        if (!regex.test(inputValue)) {
            $(this).val('');
            Swal.fire({
                icon: 'warning',
                title: 'Only text Allowed',
                text: "Sorry, Please enter text only - No numbers or Special Characters",
                footer: '<a href="/">Sign Out</a>'
            });
        }
    })

    $('.select2').select2()

})
