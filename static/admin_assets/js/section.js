$(document).ready(function () {
    // On change get all details related to pincode
    $('#pincode').on('blur', function () {
        $('#village').empty()
        $('#village').append(`<option value = '' class = 'spinner-border' role="status"> 
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
                $('#village').empty()
                if (html.Message == 'No records found') {
                    Swal.fire({
                        title: "Wrong Pincode",
                        text: "Please Enter Correct Pincode",
                        icon: "info"
                    });
                } else {

                    let PostOffice = html.result
                    $('#village').append(`<option value = ''> -- Select Village -- </option>`)
                    $(PostOffice).each(function (index, post_val) {
                        $('#village').append(`<option value = '${post_val.postalLocation}' data-hidden = '${post_val.id}'>${post_val.postalLocation}</option>`)
                    })
                }
            },
            error: function (jqxhr, textStatus, error) {
            }
        });
    });

    // On change of village get all village data
    $('#village').on('change', function () {
        village_name = $('option:selected', this).attr('data-hidden');
        pincode = $('#pincode').val()


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
                            $('#taluka').val(post_val.province)
                            $('#city').val(post_val.district)
                            $('#district').val(post_val.district)
                            $('#state').val(post_val.state)
                        }
                    })
                }
            },
            error: function (jqxhr, textStatus, error) {
            }
        })
    })


    // percentage validation on section 2
    $('.percentage_validation').on('blur', function () {
        if ($(this).val() < 35) {
            Swal.fire({
                title: "Sorry",
                text: "Below 35 percentage not accepted",
                icon: "error"
            });
        }
        else if ($(this).val() > 100) {
            Swal.fire({
                title: "Wrong Percentage",
                text: "Please Enter Correct Percentage",
                icon: "info"
            });
        }
    })

    // -------------------- Populate the Subcaste on Selected Caste --------------
/*
    This is the logic of rendering subcaste on caste.
    Route call will be found in: /PythonFiles/CandidatePages/ApplicationForm/section1.py
    Caste logic is in: /Classes/caste.py
*/
document.getElementById("caste").addEventListener("change", function () {
    const selectedOption = this.options[this.selectedIndex];
    const uniqueNumber = selectedOption.getAttribute("data-hidden");
    const subcasteDropdown = document.getElementById("your_caste");

//    alert(uniqueNumber);

    // Clear the subcaste dropdown
    subcasteDropdown.innerHTML = '<option value="" selected>-- Select Subcaste --</option>';

    if (uniqueNumber) {
        // Fetch subcastes for the selected unique number
        fetch(`/get_subcastes/${uniqueNumber}`)
            .then(response => response.json())
            .then(data => {
                if (data.subcastes && data.subcastes.length > 0) {
                    data.subcastes.forEach(subcaste => {
                        const option = document.createElement("option");
                        option.value = subcaste;
                        option.textContent = subcaste;
                        subcasteDropdown.appendChild(option);
                    });
                }
            })
            .catch(error => console.error('Error fetching subcastes:', error));
    }
});
// -------------------- END Populate the Subcaste on Selected Caste -------------
    // $('#phd_registration_date').on('blur', function () {
    //     let dob = $('#dob').val()
    //     let phd_registration_date = $('#phd_registration_date').val()
    //     if (dob == '') {
    //         Swal.fire({
    //             title: "Field required",
    //             text: "Please Enter date of birth first",
    //             icon: "info"
    //         });
    //         $('#dob').val('')
    //         $('#phd_registration_date').val('')
    //     } else {
    //         let year1 = parseInt(dob.split('-')[0]);
    //         let year2 = parseInt(phd_registration_date.split('-')[0]);
    //         // Calculate the difference in years
    //         let age = year2 - year1 - 1;
    //         if (age > 45 || age < 18) {
    //             Swal.fire({
    //                 icon: 'error',
    //                 title: 'Oops...',
    //                 text: "We're sorry, but this Fellowship is only open to individuals aged 18 to 45. Thank you for your interest.",
    //                 footer: '<a href="/">Sign Out</a>'
    //             })
    //         } else {
    //             $('#age').val(age).prop('readonly', true);
    //         }
    //     }
    // })

    $('#pvtg').on('change', function(){
        if($(this).val()=='Yes'){
            $('#pvtg_caste').attr('disabled', false)
        }
        else
        {
            $('#pvtg_caste').attr('disabled', true)
        }
    })

    $('#section1').submit(function(e){
        $('#pvtg_caste').attr('disabled',false)
    })

    $('#section1 input').on('keypress', function (e) {
        if (e.which == 13 || e.which == 10) {
            e.preventDefault();  // Fix the typo here
            return false;
        }
    });

    $('#adhaar_seeding_bank').on('change', function () {
        var inputValue = $(this).val();
        // Test if the input value contains only text
        if (inputValue == 'No') {
            Swal.fire({
                icon: 'warning',
                title: 'This is Mandatory - Please send within 15 Days',
                text: "Please send the document within in 10 days after submission of Form to - it_helpdesk@icspune.com",
                footer: '<a href="/">Sign Out</a>'
            });
        }
    })


   $(document).ready(function () {
        const $aadhaarField = $("#aadhaar");
        const $form = $aadhaarField.closest("form");
        const $verifyButton = $(".btn-primary");
        let isAadhaarVerified = false; // Flag to track Aadhaar verification status

        // Disable all inputs except Aadhaar initially
        function disableAllInputsExceptAadhaar() {
            $form.find("input, button, select, textarea").not($aadhaarField).not($verifyButton).prop("disabled", true);
        }

        // Enable all inputs after Aadhaar is verified
        function enableAllInputs() {
            $form.find("input, button, select, textarea").prop("disabled", false);
        }

        // Event listener for Verify Aadhaar button
        $verifyButton.on("click", function (e) {
            e.preventDefault(); // Prevent default button behavior

            const aadhaarValue = $aadhaarField.val();
            if (aadhaarValue.length === 12 && /^[0-9]{12}$/.test(aadhaarValue)) {
                // Make AJAX call for Aadhaar verification
                $.ajax({
                    // url: "http://fellowship.trti-maha.in:8080/", // Replace with your actual API endpoint
                    url: "http://fellowship.trti-maha.in:8080/", // Replace with your actual API endpoint
                    method:"POST",
                    data:{entered_uid: aadhaarValue, entered_url: window.location.href, entered_opr:'struid'},  // Automatically sends as query string
                    beforeSend: function () {
                        $verifyButton.text("Verifying...").prop("disabled", true); // Indicate verification in progress
                    },
                    success: function (response) {
                        // If response is already a JSON object, no need to parse it
                        // If response is a string, you can use JSON.parse(response)
                        var response_data = response; // Assuming the response is already parsed as JSON

                        // Optionally alert a more readable version of the response data
                        // alert(JSON.stringify(response_data, null, 2)); // This will format the JSON response in a readable way

                        if (response_data.Status === true && response_data.refnum !== null) {
                            Status = true;
                            Swal.fire({
                                icon: 'success',
                                title: 'Aadhaar Verified Successfully',
                                text: "Entered Aadhaar Number from " + window.location.href + " URL has been verified successfully.",
                                footer: '<a href="/">Sign Out</a>'
                            });
                            enableAllInputs(); // Enable all fields after verification
                            $('#aadhaar').hide(); // Hide the Aadhaar input field
                            $('#aadhaarVerificationStatus').html('<i class="bi bi-check-circle-fill" style="color: green;"></i> Verified'); // Display tick and "Verified"
                            $('#aadhaarVerificationStatus').show(); // Show the status message
                            $verifyButton.hide(); // Show the status message
                            $('#aadhaar_refnum').val(response_data.refnum);
                        } else if (response_data.refnum === null || response_data.refnum === '') {
                            Swal.fire({
                                icon: 'error',
                                title: 'Aadhaar Not Verified',
                                text: 'Aadhaar is not verified. Please enter a valid Aadhaar number.',
                                footer: '<a href="#">Try Again</a>'
                            });
                            $('#aadhaar').val('');
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Aadhaar Verification Failed',
                                text: 'Aadhaar verification failed. Please try again.',
                                footer: '<a href="#">Retry</a>'
                            });
                            $('#aadhaar').val('');
                        }
                    },
                    error: function (xhr, status, error) {
                        if (xhr.status === 500) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Aadhaar Verification Error',
                                text: 'The Aadhaar number entered is not valid. Please enter a valid Aadhaar number.',
                                footer: '<a href="#">Retry</a>'
                            });
                            $('#aadhaar').val('');
                        } else {
                            Swal.fire({
                                icon: 'error',
                                title: 'Something Went Wrong',
                                text: 'An unexpected error occurred. Aadhaar number entered is not valid. Please try again.',
                                footer: '<a href="#">Try Again</a>'
                            });
                            $('#aadhaar').val('');
                        }
                        $verifyButton.prop("disabled", false).text("Verify Aadhaar"); // Re-enable the button on error
                    },
                    complete: function () {
                        $verifyButton.text("Verify Aadhaar").prop("disabled", false); // Reset button state
                    }
                });
            } else {
                alert("Please enter a valid 12-digit Aadhaar number before verifying.");
            }
        });

        // Initially disable inputs until Aadhaar is verified
        disableAllInputsExceptAadhaar();
    });



})




