function validateField(element) {
  min = parseInt(element.getAttribute("minlength"));
  max = parseInt(element.getAttribute("maxlength"));
  field_value = element.value;
  field_name = element.getAttribute("data-name");

  if (field_value.length < min || field_value.length > max) {
    Swal.fire({
      icon: "error",
      title: "Oops...",
      text: `${field_name} must be between ${min} and ${max} characters!`,
      footer: '<a href="#">Why do I have this issue?</a>',
    });
    element.value = "";
  }
}

function validatePercentage(input) {

  input.value = input.value.replace(/[^\d.]/g, "");


  const decimalParts = input.value.split(".");

  if (decimalParts[1].length == 0) {
    input.value = input.value.slice(0, 2) + '.00';
  }
}


function validateMobileNumber(input) {

  let cleanedValue = input.value.replace(/\D/g, '');


  if (cleanedValue.startsWith('0')) {

    cleanedValue = cleanedValue.substring(1);
  }

  cleanedValue = cleanedValue.substring(0, 10);

  input.value = cleanedValue;
}

function validateGender(inputField) {
  var enteredValue = inputField.value.toLowerCase();

  // Array of valid gender options
  var validGenders = ['male', 'female', 'other'];

  // Check if the entered value is one of the valid options
  if (validGenders.includes(enteredValue)) {
    // Valid gender entered
    console.log('Valid gender: ' + enteredValue);
  } else {
    // Invalid gender entered
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Invalid gender! Please enter Male, Female, or Other.',
      footer: '<a href="#">Why do I have this issue?</a>',
    });

    // Optionally, you can clear the input or take other actions as needed
    inputField.value = '';
  }
}

function validateAnswer(inputField) {
  var enteredValue = inputField.value.toLowerCase();

  // Array of valid gender options
  var validAnswers = ['yes', 'no'];

  // Check if the entered value is one of the valid options
  if (validAnswers.includes(enteredValue)) {
    // Valid gender entered
    console.log('Valid answer: ' + enteredValue);
  } else {
    // Invalid gender entered
    Swal.fire({
      icon: 'error',
      title: 'Oops...',
      text: 'Invalid Answer! Please enter Yes or No.',
      footer: '<a href="#">Why do I have this issue?</a>',
    });

    // Optionally, you can clear the input or take other actions as needed
    inputField.value = '';
  }
}


function validateForm() {
  alert('Hi')
  // Array of field IDs to check
  var fieldIdsToCheck = [
    "applicant_id", "first_name", "middle_name", "last_name", "mobile_number", "email", "date_of_birth",
    "gender", "age", "caste", "your_caste", "marital_status", "add_1", "add_2", "pincode", "village", "taluka", "district",
    "state", "city", "phd_registration_date", "concerned_university", "topic_of_phd",
    "name_of_guide", "name_of_college", "stream", "board_university", "admission_year", "passing_year", "percentage",
    "family_annual_income", "income_certificate_number", "issuing_authority", "domicile", "domicile_certificate",
    "domicile_number", "caste_certf", "issuing_district", "caste_issuing_authority", "salaried", "disability",
    "father_name", "mother_name", "work_in_government", "bank_name", "account_number", "ifsc_code",
    "account_holder_name"
  ];

  for (var i = 0; i < fieldIdsToCheck.length; i++) {
    var fieldId = fieldIdsToCheck[i];
    var fieldElement = document.getElementById(fieldId);
    var fieldValue = fieldElement.value.trim();

    // Check if the field is disabled
    var isDisabled = fieldElement.disabled;

    if (isDisabled && fieldValue.toLowerCase() === 'none') {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: `Please fill in the ${fieldId.replace(/_/g, ' ')} field before submission.`,
        footer: '<a href="#">Why do I have this issue?</a>',
      });

      hasNoneValue = true;
      // Optionally, you can clear the field or take other actions as needed
      fieldElement.value = '';
    }
  }


  if (hasNoneValue) {
    return false;
  }

  // Add similar checks for other fields if needed

  // Call your existing validation functions for other fields
  validateField(document.getElementById("other_field_id"));
  // Call other validation functions as needed

  return true;
}
