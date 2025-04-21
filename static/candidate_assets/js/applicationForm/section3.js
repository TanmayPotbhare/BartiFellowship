function validateIncome() {
    var incomeInput = document.getElementById('family_annual_income');
    var income = incomeInput.value;

    // Remove any non-numeric characters
    incomeInput.value = incomeInput.value.replace(/[^0-9]/g, '');

    // Limit the input to 6 digits
    if (incomeInput.value.length > 10) {
        incomeInput.value = incomeInput.value.slice(0, 10);
    }

    // Prevent the number from starting with 0s
    if (incomeInput.value.startsWith('0') && incomeInput.value.length > 1) {
        Swal.fire({
            title: "Invalid Input!",
            text: "Income cannot start with zero.",
            icon: "error"
        });
        incomeInput.value = '';
        return;
    }

    // Limit the input to 6 digits
    if (incomeInput.value.length < 4) {
        Swal.fire({
            title: "Invalid Input!",
            text: "Income must be atleast four digits.",
            icon: "error"
        });
        incomeInput.value = '';
    }

    // Check if income exceeds 8 Lacs (8,00,000)
    // if (parseInt(incomeInput.value) > 800000) {
    //     // If income is more than 8 Lacs, show a popup message
    //     Swal.fire({
    //                 title: "Income Criteria Not Met!",
    //                 text: "To be eligible for the fellowship, the income must be less than or equal to 8 lakhs.",
    //                 icon: "error"
    //             });
    //     incomeInput.value = ''; // Reset the input field
    // }
    if (parseInt(incomeInput.value) <= 0) {
        // If income is more than 8 Lacs, show a popup message
        Swal.fire({
                    title: "Income Criteria Not Met!",
                    text: "Family Annual Income cannot be zero.",
                    icon: "error"
                });
        incomeInput.value = ''; // Reset the input field
    }
}


function validateIncomeCertificateNumber() {
    var incomeCertificateInput = document.getElementById('income_certificate_number');
    var incomeCertificateNumber = incomeCertificateInput.value;

    // Remove any non-numeric characters
    incomeCertificateInput.value = incomeCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (incomeCertificateInput.value.length > 20){
        incomeCertificateInput.value = incomeCertificateInput.value.slice(0, 20);
    }
}


function validateDomicileCertificateNumber() {
    var domicileCertificateInput = document.getElementById('domicile_number');
    var domicileCertificateNumber = domicileCertificateInput.value;

    // Remove any non-numeric characters
    domicileCertificateInput.value = domicileCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (domicileCertificateInput.value.length > 20){
        domicileCertificateInput.value = domicileCertificateInput.value.slice(0, 20);
    }
}



function validateCasteCertificateNumber() {
    var casteCertificateInput = document.getElementById('caste_certf_number');
    var casteCertificateNumber = casteCertificateInput.value;

    // Remove any non-numeric characters
    casteCertificateInput.value = casteCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (casteCertificateInput.value.length > 20){
        casteCertificateInput.value = casteCertificateInput.value.slice(0, 20);
    }
}


function validateValidityCertificateNumber() {
    var validityCertificateInput = document.getElementById('validity_cert_number');
    var validityCertificateNumber = validityCertificateInput.value;

    // Remove any non-numeric characters
    validityCertificateInput.value = validityCertificateNumber.replace(/[^0-9]/g, '');

    // Ensure length is exactly 20 characters
    if (validityCertificateInput.value.length > 20){
        validityCertificateInput.value = validityCertificateInput.value.slice(0, 20);
    }
}


document.getElementById('income_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('income_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('domicile_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('domicile_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('caste_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


document.getElementById('validity_issuing_district').addEventListener('change', function() {
    const districtId = this.selectedOptions[0].getAttribute('data-hidden');
    fetch(`/get_talukas/${districtId}`)
        .then(response => response.json())
        .then(data => {
            const talukaSelect = document.getElementById('validity_issuing_taluka');
            talukaSelect.innerHTML = '<option value="">-- Select Taluka --</option>'; // Reset taluka dropdown
            data.talukas.forEach(taluka => {
                const option = document.createElement('option');
                option.value = taluka;
                option.textContent = taluka;
                talukaSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching talukas:', error));
});


// $('#domicile').on('change', function () {
//     if($(this).val() == 'Yes'){
//         $('#domicile_number').attr('disabled',false)
//         $('#domicile_issuing_authority').attr('disabled',false)
//         $('#domicile_issuing_district').attr('disabled',false)
//         $('#domicile_issuing_taluka').attr('disabled',false)
//         $('#domicile_barcode').attr('disabled',false)
//     }else if($(this).val() == 'No'){
//         Swal.fire({
//                 title: "Sorry!",
//                 text: "Sorry, you cannot apply for the Fellowship. A Domicile Certificate is mandatory.Thank you for your interest.",
//                 icon: "error"
//             });
//         $('#domicile_number').attr('disabled',true)
//         $('#domicile_issuing_authority').attr('disabled',true)
//         $('#domicile_issuing_district').attr('disabled',true)
//         $('#domicile_issuing_taluka').attr('disabled',true)
//         $('#domicile_barcode').attr('disabled',true)
//         $('#domicile').val('')
//         $('#domicile_number').val('')
//         $('#domicile_issuing_authority').val('')
//         $('#domicile_issuing_district').val('')
//         $('#domicile_issuing_taluka').val('')
//         $('#domicile_barcode').val('')
//     }
// })

$('#domicile').on('change', function () {
    if ($(this).val() == 'Yes') {
        $('#domicile_number').removeClass('disable');
        $('#domicile_issuing_authority').removeClass('disable');
        $('#domicile_issuing_district').removeClass('disable');
        $('#domicile_issuing_taluka').removeClass('disable');
        $('#domicile_barcode').removeClass('disable');
         $('#domicile_number').prop('disabled', false);
        $('#domicile_issuing_authority').prop('disabled', false);
        $('#domicile_issuing_district').prop('disabled', false);
        $('#domicile_issuing_taluka').prop('disabled', false);
        $('#domicile_barcode').prop('disabled', false);

    } else if ($(this).val() == 'No') {
        Swal.fire({
            title: "Sorry!",
            text: "Sorry, you cannot apply for the Fellowship. A Domicile Certificate is mandatory. Thank you for your interest.",
            icon: "error"
        });
        $('#domicile_number').addClass('disable');
        $('#domicile_issuing_authority').addClass('disable');
        $('#domicile_issuing_district').addClass('disable');
        $('#domicile_issuing_taluka').addClass('disable');
        $('#domicile_barcode').addClass('disable');

        $('#domicile_number').prop('disabled', true);
        $('#domicile_issuing_authority').prop('disabled', true);
        $('#domicile_issuing_district').prop('disabled', true);
        $('#domicile_issuing_taluka').prop('disabled', true);
        $('#domicile_barcode').prop('disabled', true);


        $('#domicile').val('');
        $('#domicile_number').val('');
        $('#domicile_issuing_authority').val('');
        $('#domicile_issuing_district').val('');
        $('#domicile_issuing_taluka').val('');
        $('#domicile_barcode').val('');
    }
});



// $('#caste_certf').on('change', function () {
//     if($(this).val() == 'Yes'){
//         $('#caste_certf_number').attr('disabled',false)
//         $('#caste_issuing_authority').attr('disabled',false)
//         $('#issuing_district').attr('disabled',false)
//         $('#caste_issuing_taluka').attr('disabled',false)
//         $('#caste_barcode').attr('disabled',false)
//     }else if($(this).val() == 'No'){
//         Swal.fire({
//                 title: "Sorry!",
//                 text: "Sorry, you cannot apply for the Fellowship. A Caste Certificate is mandatory.Thank you for your interest.",
//                 icon: "error"
//             });
//         $('#caste_certf_number').attr('disabled',true)
//         $('#caste_issuing_authority').attr('disabled',true)
//         $('#issuing_district').attr('disabled',true)
//         $('#caste_issuing_taluka').attr('disabled',true)
//         $('#caste_barcode').attr('disabled',true)

//         $('#caste_certf').val('')
//         $('#caste_certf_number').val('')
//         $('#caste_issuing_authority').val('')
//         $('#issuing_district').val('')
//         $('#caste_issuing_taluka').val('')
//         $('#caste_barcode').val('')
//     }
// })



$('#caste_certf').on('change', function () {
    if ($(this).val() == 'Yes') {
        $('#caste_certf_number').removeClass('disable');
        $('#caste_issuing_authority').removeClass('disable');
        $('#issuing_district').removeClass('disable');
        $('#caste_issuing_taluka').removeClass('disable');
        $('#caste_barcode').removeClass('disable');

        $('#caste_certf_number').prop('disabled', false);
        $('#caste_issuing_authority').prop('disabled', false);
        $('#issuing_district').prop('disabled', false);
        $('#caste_issuing_taluka').prop('disabled', false);
        $('#caste_barcode').prop('disabled', false);

    } else if ($(this).val() == 'No') {
        Swal.fire({
            title: "Sorry!",
            text: "Sorry, you cannot apply for the Fellowship. A Caste Certificate is mandatory. Thank you for your interest.",
            icon: "error"
        });
        $('#caste_certf_number').addClass('disable');
        $('#caste_issuing_authority').addClass('disable');
        $('#issuing_district').addClass('disable');
        $('#caste_issuing_taluka').addClass('disable');
        $('#caste_barcode').addClass('disable');

        $('#caste_certf_number').prop('disabled', true);
        $('#caste_issuing_authority').prop('disabled', true);
        $('#issuing_district').prop('disabled', true);
        $('#caste_issuing_taluka').prop('disabled', true);
        $('#caste_barcode').prop('disabled', true);

        $('#caste_certf').val('');
        $('#caste_certf_number').val('');
        $('#caste_issuing_authority').val('');
        $('#issuing_district').val('');
        $('#caste_issuing_taluka').val('');
        $('#caste_barcode').val('');
    }
});


// $('#validity_certificate').on('change', function () {
//     if($(this).val() == 'Yes'){
//         $('#validity_cert_number').attr('disabled',false).prop('required', true);
//         $('#validity_issuing_authority').attr('disabled',false).prop('required', true);
//         $('#validity_issuing_district').attr('disabled',false).prop('required', true);
//         $('#validity_issuing_taluka').attr('disabled',false).prop('required', true);
//         $('#validity_barcode').attr('disabled',false).prop('required', true);

//     }else if($(this).val() == 'No'){
//         $('#validity_cert_number').attr('disabled',true).prop('required', false);
//         $('#validity_issuing_authority').attr('disabled',true).prop('required', false);
//         $('#validity_issuing_district').attr('disabled',true).prop('required', false);
//         $('#validity_issuing_taluka').attr('disabled',true).prop('required', false);
//         $('#validity_barcode').attr('disabled',true).prop('required', false);

//         $('#validity_cert_number').val('')
//         $('#validity_issuing_authority').val('')
//         $('#validity_issuing_district').val('')
//         $('#validity_issuing_taluka').val('')
//         $('#validity_barcode').val('')
//     }
// })



$('#validity_certificate').on('change', function () {
    if ($(this).val() == 'Yes') {
        $('#validity_cert_number').removeClass('disable').prop('required', true);
        $('#validity_issuing_authority').removeClass('disable').prop('required', true);
        $('#validity_issuing_district').removeClass('disable').prop('required', true);
        $('#validity_issuing_taluka').removeClass('disable').prop('required', true);
        $('#validity_barcode').removeClass('disable').prop('required', true);

         $('#validity_cert_number').prop('disabled', false);
        $('#validity_issuing_authority').prop('disabled', false);
        $('#validity_issuing_district').prop('disabled', false);
        $('#validity_issuing_taluka').prop('disabled', false);
        $('#validity_barcode').prop('disabled', false);

    } else if ($(this).val() == 'No') {
        $('#validity_cert_number').addClass('disable').prop('required', false);
        $('#validity_issuing_authority').addClass('disable').prop('required', false);
        $('#validity_issuing_district').addClass('disable').prop('required', false);
        $('#validity_issuing_taluka').addClass('disable').prop('required', false);
        $('#validity_barcode').addClass('disable').prop('required', false);

        $('#validity_cert_number').prop('disabled', true);
        $('#validity_issuing_authority').prop('disabled', true);
        $('#validity_issuing_district').prop('disabled', true);
        $('#validity_issuing_taluka').prop('disabled', true);
        $('#validity_barcode').prop('disabled', true);

        $('#validity_cert_number').val('');
        $('#validity_issuing_authority').val('');
        $('#validity_issuing_district').val('');
        $('#validity_issuing_taluka').val('');
        $('#validity_barcode').val('');
    }
});


// Function to enable or disable the submit button
function enableDisabledFields3() {
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
    document.getElementById("verifyDetails").addEventListener('change', enableDisabledFields);
    document.getElementById("verifyDetailsHindi").addEventListener('change', enableDisabledFields);

    // Call function initially to check if the button should be enabled or not
    enableDisabledFields2();
};

// ----------------------------------------------------
function toggleDomicileBarcodefield(select) {
    
    const domicileDiv = document.getElementById('domicile_num_div');
    const numberField = document.getElementById('domicile_number');

    const issueDateDiv = document.getElementById('domicile_isssue_date_div');
    const issueDateField = document.getElementById('domicile_barcode_issue_date');

    if (select.value === 'Yes') {
        
        domicileDiv.classList.remove('d-none'); // Show field
        numberField.setAttribute('required', 'required');

        issueDateDiv.classList.add('d-none'); // Show field
        issueDateField.removeAttribute('required');
        issueDateField.value = ''; // Clear input field

    } else {
       
        domicileDiv.classList.add('d-none'); // Hide field
        numberField.value = ''; // Clear input field
        numberField.removeAttribute('required');

        issueDateDiv.classList.remove('d-none'); // Hide field
        issueDateField.setAttribute('required', 'required');

    }
}
// ----------------------------------------------------

// ----------------------------------------------------
function toggleCasteBarcodefield(select) {
    
    const casteDiv = document.getElementById('caste_num_div');
    const numberField = document.getElementById('caste_certf_number');

    const issueDateDiv = document.getElementById('caste_issue_date_div');
    const issueDateField = document.getElementById('caste_barcode_issue_date');

    if (select.value === 'Yes') {
        
        casteDiv.classList.remove('d-none'); // Show field
        numberField.setAttribute('required', 'required');

        issueDateDiv.classList.add('d-none'); // Show field
        issueDateField.removeAttribute('required');
        issueDateField.value = ''; // Clear input field

    } else {
       
        casteDiv.classList.add('d-none'); // Hide field
        numberField.value = ''; // Clear input field
        numberField.removeAttribute('required');

        issueDateDiv.classList.remove('d-none'); // Hide field
        issueDateField.setAttribute('required', 'required');

    }
}
// ----------------------------------------------------

// ----------------------------------------------------
function toggleValidityBarcodefield(select) {
    
    const validityDiv = document.getElementById('validity_num_div');
    const numberField = document.getElementById('validity_cert_number');

    const issueDateDiv = document.getElementById('validity_issue_date_div');
    const issueDateField = document.getElementById('validity_barcode_issue_date');

    if (select.value === 'Yes') {
        
        validityDiv.classList.remove('d-none'); // Show field
        numberField.setAttribute('required', 'required');

        issueDateDiv.classList.add('d-none'); // Show field
        issueDateField.removeAttribute('required');
        issueDateField.value = ''; // Clear input field

    } else {
       
        validityDiv.classList.add('d-none'); // Hide field
        numberField.value = ''; // Clear input field
        numberField.removeAttribute('required');

        issueDateDiv.classList.remove('d-none'); // Hide field
        issueDateField.setAttribute('required', 'required');

    }
}
// ----------------------------------------------------


// ----------------------------------------------------
function toggleIncomeBarcodefield(select) {
    
    const incomeDiv = document.getElementById('income_number_div');
    const numberField = document.getElementById('income_certificate_number');

    const issueDateDiv = document.getElementById('income_issue_date_div');
    const issueDateField = document.getElementById('income_barcode_issue_date');

    if (select.value === 'Yes') {
        
        incomeDiv.classList.remove('d-none'); // Show field
        numberField.setAttribute('required', 'required');

        issueDateDiv.classList.add('d-none'); // Show field
        issueDateField.removeAttribute('required');
        issueDateField.value = ''; // Clear input field

    } else if (select.value === 'No'){
       
        incomeDiv.classList.add('d-none'); // Hide field
        numberField.value = ''; // Clear input field
        numberField.removeAttribute('required');

        issueDateDiv.classList.remove('d-none'); // Hide field
        issueDateField.setAttribute('required', 'required');

    }
}

function editDomicileDetails() {
    $('#domicile_barcode').removeClass('disable').prop('disabled', false);
    $('#domicile_number').removeClass('disable').prop('disabled', false);
    $('#domicile_issuing_authority').removeClass('disable').prop('disabled', false);
    $('#domicile_issuing_district').removeClass('disable').prop('disabled', false);
    $('#domicile_issuing_taluka').removeClass('disable').prop('disabled', false);
}

function editCasteDetails() {
    $('#caste_barcode').removeClass('disable').prop('disabled', false);
    $('#caste_certf_number').removeClass('disable').prop('disabled', false);
    $('#caste_issuing_authority').removeClass('disable').prop('disabled', false);
    $('#issuing_district').removeClass('disable').prop('disabled', false);
    $('#caste_issuing_taluka').removeClass('disable').prop('disabled', false);
}

function editValidityDetails() {
    $('#validity_barcode').removeClass('disable').prop('disabled', false);
    $('#validity_cert_number').removeClass('disable').prop('disabled', false);
    $('#validity_issuing_authority').removeClass('disable').prop('disabled', false);
    $('#validity_issuing_district').removeClass('disable').prop('disabled', false);
    $('#validity_issuing_taluka').removeClass('disable').prop('disabled', false);
    $('#validity_certificate').val('');
}


// --------------------1--------------------------------
