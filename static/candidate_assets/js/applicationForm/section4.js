// This function is for PVTG Caste
function toggleGovField(select) {
    
    const numberDiv = document.getElementById('open_no_of_gov_emp');
    const numberField = document.getElementById('no_of_gov_employee');

    if (select.value === 'Yes') {
        
        numberDiv.classList.remove('d-none'); // Show field
        numberField.setAttribute('required', 'required');

    } else {
       
        numberDiv.classList.add('d-none'); // Hide field
        numberField.value = ''; // Clear input field
        numberField.removeAttribute('required');

        // Hide all employee details and remove required attributes
        toggleEmployeeFields(0);

    }
}
// ----------------------------------------------------------------


function toggleEmployeeFields(count) {
    const fields = ['name_emp', 'position_emp', 'relation_emp'];

    for (let i = 1; i <= 3; i++) {
        fields.forEach(field => {
            const element = document.getElementById(`${field}_${i}`);
            const input = document.getElementById(`${field}_${i}`).querySelector('input');

            if (i <= count) {
                element.classList.remove('d-none'); // Show field
                input.setAttribute('required', 'required'); // Set required
            } else {
                element.classList.add('d-none'); // Hide field
                input.removeAttribute('required'); // Remove required
                input.value = ''; // Clear input value
            }
        });
    }
}

// Event listener for Number of Government Employees dropdown
document.getElementById('no_of_gov_employee').addEventListener('change', function () {
    const selectedValue = parseInt(this.value, 10) || 0;
    toggleEmployeeFields(selectedValue);
});



// ----------- Account Number validation -------------------
function validateAccountNumber() {
    var accountNumberInput = document.getElementById('account_number');
    var accountNumberNumber = accountNumberInput.value;

    // Remove any non-numeric characters
    accountNumberInput.value = accountNumberNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (accountNumberInput.value.length > 20){
        accountNumberInput.value = accountNumberInput.value.slice(0, 20);
    }
}
// ---------------------------------------------------------


// ----------- Account Holder Name validation -------------------
function validateAccountHolderName() {
    const nameInput = document.getElementById('account_holder_name');
    const nameValue = nameInput.value.trim();

    // Split the input by spaces and filter out empty parts
    const words = nameValue.split(/\s+/).filter(word => word);

    if (words.length < 3 || words.length > 3) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Name Detected',
            text: 'Please enter First Name, Middle Name and Surname.'
        });
        nameInput.value = ''; // Clear the input field
        nameInput.focus();
        return false;
    }

    // Check for non-alphabetic characters (optional)
    const validName = /^[a-zA-Z\s]+$/.test(nameValue);
    if (!validName) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Langauge Detected',
            text: 'The Account Holder Name should only contain letters and spaces.'
        });
        nameInput.value = ''; // Clear the input field
        nameInput.focus();
        return false;
    }

    return true;
}
// ---------------------------------------------------------


// ----------- IFSC Code validation -------------------
function validateIFSC() {
    const ifscInput = document.getElementById('ifsc_code');
    const bank_nameInput = document.getElementById('bank_name');
    const micrInput = document.getElementById('micr');
    const ifscValue = ifscInput.value.trim();

    // Regular expression for IFSC Code validation
    const ifscRegex = /^[A-Z]{4}0[A-Z0-9]{6}$/;

    if (!ifscRegex.test(ifscValue)) {
        Swal.fire({
            title: "Invalid IFSC Code",
            text: "The IFSC Code should be exactly 11 characters long, starting with 4 alphabets, followed by 0, and ending with 6 alphanumeric characters.",
            icon: "info",
            confirmButtonText: "Okay",
            customClass: {
                confirmButton: 'btn btn-primary'
            }
        }).then(() => {
            ifscInput.value = ''; // Clear the input field
            bank_nameInput.value = ''; // Clear the input field
            micrInput.value = ''; // Clear the input field
            ifscInput.focus(); // Bring focus back to the input
        });
        return false;
    }

    return true;
}
// ---------------------------------------------------------


// ----------- Autopopulate BAnk name and micr validation -------------------
$('#ifsc_code').on('blur', function () {
    let ifsc = $(this).val()
    $.ajax({
        url: "/get_ifsc_data",
        type: "GET",
        data: { 'ifsc': ifsc },
        success: function (html) {
            $('#bank_name').val(html.BANK)
            $('#micr').val(html.MICR)
        }
    })
})
// ---------------------------------------------------------

function showAlert() {
    Swal.fire({
        icon: 'warning',
        title: 'Incomplete Sections',
        text: 'Please complete the current section before proceeding to the next.',
        confirmButtonText: 'OK'
    });
}

// Function to enable or disable the submit button
function enableDisabledFields4() {
    const checkbox1 = document.getElementById("verifyDetails");
    const checkbox2 = document.getElementById("verifyDetailsHindi");

    //  Uncomment below checkboxes while enabling the self declaration for Salary in section 4
    const checkbox3 = document.getElementById("verifySalaryDeclaration");
    const checkbox4 = document.getElementById("verifySalaryDeclarationMarathi");
    const submitBtn = document.getElementById("submit");

    // Enable the button if both checkboxes are checked
    if (checkbox1.checked && checkbox2.checked && checkbox3.checked && checkbox4.checked) {
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
    document.getElementById("verifySalaryDeclaration").addEventListener('change', enableDisabledFields2);
    document.getElementById("verifySalaryDeclarationMarathi").addEventListener('change', enableDisabledFields2);

    // Call function initially to check if the button should be enabled or not
    enableDisabledFields3();
};

// This function is for PVTG Caste
function toggleDisabilityField(select) {
    const disability_div = document.getElementById('disability_type_div');
    const disability_feild = document.getElementById('type_of_disability');
    const disability_perc_div = document.getElementById('disability_perc_div');
    const disability_perc_feild = document.getElementById('perc_of_disability');

    if (select.value === 'Yes') {
        disability_div.classList.remove('d-none'); // Show field
        disability_feild.setAttribute('required', 'required');
        disability_perc_div.classList.remove('d-none'); // Show field
        disability_perc_feild.setAttribute('required', 'required');
    } else {
        disability_div.classList.add('d-none'); // Hide field
        disability_feild.removeAttribute('required');
        disability_feild.value = ''; // Clear input field
        disability_perc_div.classList.add('d-none'); // Show field
        disability_perc_feild.removeAttribute('required', 'required');
        disability_perc_feild.value = ''; // Clear input field
    }
}

// ------------- Salaried Validation  --------------
// ------------------- Start -----------------------
$('#salaried').on('change', function () {
    if($(this).val() == 'Yes'){
        Swal.fire({
            title: "Sorry!",
            text: "Sorry, you cannot apply for the Fellowship. Salaried candidates are not eligible to apply for the Fellowship. Thank you for your interest.",
            icon: "error"
        });
        $('#salaried').val('')
    }
});
// ------------------------------------------------

// ------------- Validate Percentage of Disability --------------
// ------- Start --------
// function validateDisabilityPercentage(input) {
//     // Allow only numeric characters and a single decimal point
//     input.value = input.value.replace(/[^0-9.]/g, '');

//     // Prevent multiple decimal points
//     if ((input.value.match(/\./g) || []).length > 1) {
//         input.value = input.value.substring(0, input.value.lastIndexOf('.'));
//     }

//     // Limit to three digits before the decimal point and two digits after
//     const regex = /^(\d{1,3})(\.\d{0,2})?$/;
//     if (!regex.test(input.value)) {
//         input.value = input.value.slice(0, -1);
//     }

//     // Ensure the value does not exceed 100.00
//     if (parseFloat(input.value) > 100) {
//         input.value = "100.00";
//     }
//     // Ensure the value does not exceed 100.00
//     if (parseFloat(input.value) < 40) {
//         Swal.fire({
//             title: "Sorry!",
//             text: "Candidates with a disability percentage less than 40% are not eligible to apply under the Disabled category",
//             icon: "error"
//         });
//         input.value = '';
//     }
//     // Zero cannot be entered in Percentage
//     if (input.value === '0') {
//         input.value = '';
//     } 
// }
// ------------------------------------------------

// ------------- Validate Percentage of Disability --------------
// ------- Start --------
$('#perc_of_disability').on('change', function () {
    if($(this).val() == 'No'){
        Swal.fire({
            title: "Sorry!",
            text: "Candidates with a disability percentage less than 40% are not eligible to apply under the Disabled category.",
            icon: "error"
        });
        $('#perc_of_disability').val('')
    }
});
// ------------------------------------------------