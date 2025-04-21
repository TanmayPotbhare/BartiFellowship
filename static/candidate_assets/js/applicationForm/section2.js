// ------------- Year Validation --------------
// ------- Start --------
function validateYear(input) {
    const currentYear = new Date().getFullYear();

    // Remove non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Limit input to 4 digits
    if (input.value.length > 4) {
        input.value = input.value.slice(0, 4);
    }

    if (input.value.length < 4) {
        Swal.fire({
            title: "Invalid Input!",		
            text: "Please Enter a 4-digit Passing Year",
            icon: "info"
        });
        input.value = '';
        return;
    }

    const inputYear = parseInt(input.value);

    // Ensure the year is not greater than the current year
    if (inputYear > currentYear) {
        Swal.fire({
            icon: "error",
            title: "Invalid Input!",
            text: "Passing Year cannot be greater than the Current Year.",
        });
        input.value = '';
        return;
    }

    // Ensure that entered year is not "0"
    if (inputYear == 0) {
        Swal.fire({
            icon: "error",
            title: "Invalid Input!",
            text: "Passing Year cannot be Zero.",
        });
        input.value = '';
        return;
    }

    if (input.value.startsWith('0')) {
        input.value = ''; // Remove the leading '0'
    }

    // Qualification order
    const qualificationOrder = [
        'ssc_passing_year',
        'hsc_passing_year',
        'graduation_passing_year',
        'phd_passing_year',
    ];

    // Get the current input's position in the order
    const inputId = input.id;
    const inputIndex = qualificationOrder.indexOf(inputId);

    // Loop through all qualifications and validate
    let previousYear = null;
    for (let i = 0; i < qualificationOrder.length; i++) {
        const field = document.getElementById(qualificationOrder[i]);
        const fieldYear = parseInt(field.value);

        // Clear higher qualifications if the current input invalidates them
        if (i > inputIndex && !isNaN(fieldYear)) {
            if (inputYear >= fieldYear) {
                Swal.fire({
                    icon: "error",
                    title: "Invalid Sequence!",
                    text: `Passing Year for Higher Qualification must be greater than ${inputYear}.`,
                });
                field.value = ''; // Clear invalid fields
            }
        }

        // Validate the order of lower qualifications
        if (i < inputIndex && !isNaN(fieldYear)) {
            if (fieldYear >= inputYear) {
                Swal.fire({
                    icon: "error",
                    title: "Invalid Year Sequence!",
                    text: `The Passing Year for this qualification cannot be the same or earlier than the Passing Year of a previous qualification you entered.`,
                });
                input.value = ''; // Clear invalid input
                return;
            }
        }

        // Check for duplicate years
        if (i !== inputIndex && fieldYear === inputYear) {
            Swal.fire({
                icon: "error",
                title: "Duplicate Passing Year!",
                text: `Passing Year cannot be the same for two qualifications.`,
            });
            input.value = ''; // Clear invalid input
            return;
        }

        // Update the previous year
        if (i < inputIndex && !isNaN(fieldYear)) {
            previousYear = fieldYear;
        }
    }
}
// ------------------------------------------------

// ---------- For Auto populating the Day Month and Year on PHD Registration Date ----------
document.getElementById('phd_registration_date').addEventListener('blur', function () {
    const dateInput = this.value;
    const SelectedDate = new Date(this.value);
    const currentDate = new Date();
    const currentYear = currentDate.getFullYear();

    if (dateInput) {
        const selectedDate = new Date(dateInput);

        // Validate the year length (4 digits)
        const phd_year = selectedDate.getFullYear();
        if (phd_year.toString().length !== 4) {
            Swal.fire({
                icon: "error",
                title: "Invalid Input!",
                text: `The year must be a 4-digit number.`,
            });
            this.value = ''; // Clear the input field
            document.getElementById('phd_registration_day').value = '';
            document.getElementById('phd_registration_month').value = '';
            document.getElementById('phd_registration_year').value = '';
            document.getElementById('phd_registration_age').value = '';
            return;
        }

        // Check if the selected year exceeds the current year
        if (phd_year > currentYear) {
            Swal.fire({
                icon: "error",
                title: "Invalid Input!",
                text: `Ph.D. Registration Year cannot be greater than the Current Year.`,
            });
            this.value = ''; // Clear the input field
            document.getElementById('phd_registration_day').value = '';
            document.getElementById('phd_registration_month').value = '';
            document.getElementById('phd_registration_year').value = '';
            document.getElementById('phd_registration_age').value = '';
            return;
        }

        // Check if the selected year exceeds the current year
        if (SelectedDate > currentDate) {
            Swal.fire({
                icon: "error",
                title: "Invalid Input!",
                text: `Please enter a valid Ph.D. Registration Date. It must be a date on or before today.`,
            });
            this.value = ''; // Clear the input field
            document.getElementById('phd_registration_day').value = '';
            document.getElementById('phd_registration_month').value = '';
            document.getElementById('phd_registration_year').value = '';
            document.getElementById('phd_registration_age').value = '';
            return;
        }

        // Extract day, month, and year
        const day = selectedDate.getDate();
        const month = selectedDate.toLocaleString('default', { month: 'long' }); // Get full month name
        const year = selectedDate.getFullYear();

        // Populate fields
        document.getElementById('phd_registration_day').value = day;
        document.getElementById('phd_registration_month').value = month;
        document.getElementById('phd_registration_year').value = year;
    } else {
        // Clear all fields if no date is selected
        document.getElementById('phd_registration_day').value = '';
        document.getElementById('phd_registration_month').value = '';
        document.getElementById('phd_registration_year').value = '';
    }
});

// --------------------------------------------------------


// ---------------- Show and Hide Field on d-none ----------------------------
// This function is responsible for displaying and hiding the Other Faculty  option based on the Faculty selected in Section2 
function toggleAdditionalFieldFaculty(select) {
    const additionalField = document.getElementById('additionalField'); // Fixed typo
    const inputField = document.getElementById('other_faculty'); // Fixed typo in variable name

    if (select.value === 'Other') {
        additionalField.classList.remove('d-none'); // Show field
        inputField.setAttribute('required', 'true'); // Set required on input field
    } else {
        additionalField.classList.add('d-none'); // Hide field
        inputField.value = ''; // Clear input field
        inputField.removeAttribute('required'); // Remove required from input field
    }
}
// ----------------------------------------------------------------


// ---------------- Show and Hide Field on d-none ----------------------------
// This function is for College toggle
function toggleCollegeField(select) {
    const additionalField = document.getElementById('collegeField');
    const inputField = document.getElementById('other_college_name');

    if (select.value === 'Other') {
        additionalField.classList.remove('d-none'); // Show field
        inputField.setAttribute("required", true);
    } else {
        additionalField.classList.add('d-none'); // Hide field
        inputField.value = ''; // Clear input field
        inputField.required = false;
    }
}
// ----------------------------------------------------------------

// --------------------------- University Populate college names ---------------------
$('#concerned_university').on('change', function () {
    const selectedValue = $(this).val(); // Get the selected value
    const universityId = $('option:selected', this).attr('data-hidden'); // Get the data-hidden attribute

    if (selectedValue === 'Other') {
        // Handle the "Other" case and exit the function
        $('#name_of_college').empty();
        $('#name_of_college').append('<option value="Other" selected>Other</option>'); // Preselect Other
        $('#collegeField').removeClass('d-none'); // Show the "Other College" input field
        return; // Exit the function
    }

    // Proceed with AJAX for other universities
    $('#name_of_college').empty();
    $('#name_of_college').append('<option>Loading ....</option>');
    $.ajax({
        url: '/get_college_data_by_university',
        method: 'POST',
        data: { 'u_id': universityId },
        success: function (html) {
            $('#name_of_college').empty();
            $('#name_of_college').prop('required', true);
            $('#name_of_college').append('<option value="">-- Select College --</option>');
            $('#name_of_college').append('<option value="Other">Other</option>');
            html.forEach(function (item) {
                $('#name_of_college').append(`<option value="${item.college_name}">${item.college_name}</option>`);
            });
        },
        error: function () {
            Swal.fire({
                icon: "error",
                title: "Please Try Again...",
                text: `Please Select Correct University`,
            });
        }
    });
});

// 0-----------------------------------------------------------------

// ---------------- Show and Hide Field on d-none ----------------------------
function toggleUniversityChange(select) {
    const additionalUniversityField = document.getElementById('additionalFieldUniversity');
    const otherUniversityInput = document.getElementById('other_university');
    const collegeDropdown = document.getElementById('name_of_college');

    if (select.value === 'Other') {
        // Show additional university field

        additionalUniversityField.classList.remove('d-none');
        otherUniversityInput.required = true;

        // Automatically select "Other" in the college dropdown
        collegeDropdown.value = 'Other';
        toggleCollegeField(collegeDropdown);
    } else {
        // Hide additional university field
        additionalUniversityField.classList.add('d-none');
        otherUniversityInput.value = ''; // Clear input field
        otherUniversityInput.required = false;

        // Reset college dropdown
        collegeDropdown.value = '';
        toggleCollegeField(collegeDropdown);
    }
}
// ----------------------------------------------------------------

// --------------------- Calculate Age on Phd Registration Year ----------------------
function calculateAges() {
    // Get the hidden DOB year (e.g., (1996,))
    const dobYear = document.getElementById('dob_year').value.substring(0, 4); // Strip non-numeric characters
    // Get the Ph.D. registration date entered by the user
    const phdRegDate = document.getElementById('phd_registration_date').value;

    if (phdRegDate) {
        // Convert Ph.D. registration date to Date object
        const phdDate = new Date(phdRegDate);

        // Get the Ph.D. registration year
        const phdYear = phdDate.getFullYear();

        let age = phdYear - dobYear;
        // Assuming the birth month and day are Jan 1st, adjust age if the Ph.D. registration date is before the birthday in that year
        const dobMonthDay = new Date(dobYear, 0, 1); // Jan 1st as an example
        if (phdDate < dobMonthDay) {
            age -= 1; // Subtract 1 if the Ph.D. registration date is before the birthday in that year
        }

        // Display the calculated age in the "Age at Ph.D Registration" input field
        document.getElementById('phd_registration_age').value = age;

        // To prevent the user from entering invalid date
        if (age > 100) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Date!',
                text: 'Please check the date you have entered.'
            });
            document.getElementById('phd_registration_date').value = '';  
            document.getElementById('phd_registration_age').value = ''; 
            return; // Exit the function
        }
        
        if (phdYear > dobYear){
            // Calculate age
        }
        else { 
            Swal.fire({
                icon: "error",
                title: "Invalid Year!",
                text: `Ph.D. Registration Year cannot be earlier than your birth year.`,
            });
            document.getElementById('phd_registration_date').value = '';  
            document.getElementById('phd_registration_age').value = '';  
        }
        
    } else {
        // Clear the age field if the registration date is not selected
        document.getElementById('phd_registration_age').value = '';
    }
}
// ----------------------------------------------------------------

// ------------- Validate Number of Attempts --------------
// ------- Start --------
function validateAttempts(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 1 digits
        if (input.value.length > 1) {
            input.value = input.value.slice(0, 1);
        }     

        if (input.value === '0') {
            input.value = '';
        }  
    }
// ------------------------------------------------

// ------------- Validate Total Marks --------------
// ------- Start --------
function validateTotalMarks(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 4 digits
        if (input.value.length > 4) {
            input.value = input.value.slice(0, 4);
        }      
        // Zero cannot be entered in Total Marks
        if (input.value === '0') {
            input.value = '';
        } 
    }
// ------------------------------------------------

// ------------- Validate Percentage --------------
// ------- Start --------
function validatePercentage(input) {
    // Allow only numeric characters and a single decimal point
    input.value = input.value.replace(/[^0-9.]/g, '');

    // Prevent multiple decimal points
    if ((input.value.match(/\./g) || []).length > 1) {
        input.value = input.value.substring(0, input.value.lastIndexOf('.'));
    }

    // Limit to three digits before the decimal point and two digits after
    const regex = /^(\d{1,3})(\.\d{0,2})?$/;
    if (!regex.test(input.value)) {
        input.value = input.value.slice(0, -1);
    }

    // Ensure the value does not exceed 100.00
    if (parseFloat(input.value) > 100) {
        input.value = "100.00";
    }
    // Zero cannot be entered in Percentage
    if (input.value === '0') {
        input.value = '';
    } 
}
// ------------------------------------------------


// Function to enable or disable the submit button
function enableDisabledFields2() {
    const checkbox1 = document.getElementById("verifyDetails");
    const checkbox2 = document.getElementById("verifyDetailsHindi");
    const submitBtn = document.getElementById("submit");

    // Enable the button if both checkboxes are checked
    if (checkbox1.checked && checkbox2.checked) {
        submitBtn.disabled = false;
    } else {
        submitBtn.disabled = true;
    }
}

// Initialize event listeners
window.onload = function() {
    // Add event listeners for checkbox change events
    document.getElementById("verifyDetails").addEventListener('change', enableDisabledFields2);
    document.getElementById("verifyDetailsHindi").addEventListener('change', enableDisabledFields2);

    // Call function initially to check if the button should be enabled or not
    enableDisabledFields2();
};

function toggleOtherQualification() {
    const otherCheckbox = document.getElementById('otherCheckbox');
    const additionalField = document.getElementById('additionalFieldSelectQualification');
    const otherInput = document.getElementById('have_you_qualified_other');

    if (otherCheckbox.checked) {
        additionalField.classList.remove('d-none');
        otherInput.required = true;
    } else {
        additionalField.classList.add('d-none');
        otherInput.required = false;
        otherInput.value = ''; // Clear input if unch ecked
    }
}

// function validateQualifications() {
//     const checkboxes = document.querySelectorAll('input[name="qualified_exams[]"]');
//     let isChecked = false;

//     checkboxes.forEach(cb => {
//         if (cb.checked) isChecked = true;
//     });

//     const submitButton = document.getElementById('submit');
//     const qualificationHelp = document.getElementById('qualificationHelp');

//     if (!isChecked) {
//         qualificationHelp.style.display = 'block';
//         submitButton.disabled = true;
//     } else {
//         qualificationHelp.style.display = 'none';
//         submitButton.disabled = false;
//     }
// }

// // Run validation on page load and whenever checkboxes change
// window.onload = function () {
//     validateQualifications();
//     const checkboxes = document.querySelectorAll('input[name="qualified_exams[]"]');
//     checkboxes.forEach(cb => cb.addEventListener('change', validateQualifications));
// };