$(document).ready(function () {
    // SSC Passing year validation on preview page
    $('#ssc_passing_year').on('blur', function () {
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
    // HSC passing year validation
    $('#hsc_passing_year').on('blur', function () {
        let hsc_passign_year = $(this).val();
        let ssc_passing_yr = $('#ssc_passing_year').val()
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
    $('#graduation_passing_year').on('blur', function () {
        let graduation_passing_year = $(this).val();
        let ssc_passing_yr = $('#ssc_passing_year').val()
        let hsc_passing_year = $('#hsc_passing_year').val()
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
    $('#phd_passing_year').on('blur', function () {
        let phd_passing_year = $(this).val()
        let graduation_passing_year = $('#graduation_passing_year').val();
        let ssc_passing_yr = $('#ssc_passing_year').val()
        let hsc_passing_year = $('#hsc_passing_year').val()
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

    // Phd registration date \\
    $('#section2 #phd_registration_date').on('blur', function () {
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

    // Get College details by university
    $('#concerned_university').on('change', function () {
        let university_id = $('option:selected', this).attr('data-hidden')
        $('#name_of_college').empty()
        $('#name_of_college').append('<option>Loading ....</option>')
        $.ajax({
            url: '/get_college_data_by_university',
            method: 'POST',
            data: { 'u_id': university_id },
            success: function (html) {
                $('#name_of_college').empty()
                $('#name_of_college').append('<option>-- Select College --</option>')
                html.forEach(function (item) {

                    $('#name_of_college').append(`<option value="${item.college_name}">${item.college_name}</option`);

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

    $('#family_annual_income').on('blur', function () {
        let income = parseInt($(this).val())
        if(income > 800000){
            Swal.fire({
                icon: "error",
                title: "Please enter the Income less than 8Lacs to get Fellowship.",
                text: `The income should be less than 800000`,
            });
            $(this).val('')
        }
    })

    $('#section2').submit(function(e){
        $('#ssc_stream').attr('disabled',false)
    })

    $('#section2 input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });

    $('#qualified').on('change',function(){
        if($(this).val() =="OTHER"){
            $('#other_cet').removeClass('d-none')
        }else{
            $('#other_cet').addClass('d-none')
            $('#other_cet input').val('')
        }
    })

})