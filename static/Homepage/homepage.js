
// --------------------------------------------------------
//                   HOMEPAGE JS
// --------------------------------------------------------

$(document).ready(function () {
      $('.counter-value').each(function () {
        $(this).prop('Counter', 0).animate({
          Counter: $(this).text()
        }, {
          duration: 3500,
          easing: 'swing',
          step: function (now) {
            $(this).text(Math.ceil(now));
          }
        });
      });
    });
// --------------------------------------------------------
//                  END HOMEPAGE JS
// --------------------------------------------------------


// --------------------------------------------------------
//                  GR PAGE JS
// --------------------------------------------------------

var homeButton = document.getElementById("home-tab");

// Attach a click event listener to the "Home" button
homeButton.addEventListener("click", function() {
  // Load the PDF when the "Home" button is clicked
  loadPDF('static/GRAMSATHI GR 1.pdf');
});

// Function to load the PDF into the iframe
function loadPDF(pdfPath) {
  var pdfFrame = document.getElementById("pdfFrame");
  pdfFrame.src = pdfPath;
}

// --------------------------------------------------------
//                  END GR PAGE JS
// --------------------------------------------------------

// --------------------------------------------------------
//                  LOGIN & SIGNUP JS
// --------------------------------------------------------

$(document).ready(function () {
    $('#year').on('change', function () {
        var year = $('#year').val();

        if (year === '2021' || year === '2022') {
            Swal.fire({
                icon: "info",
                title: "IT SEEMS YOU ARE AN OLD USER....",
                text: `LOGIN IS ALREADY CREATED FOR YOU. Please Login with the registered email ID and Password received via Email.`,
            });

            // Clear form inputs
            $('#year').val('');
            $('#first_name').val('');
            $('#middle_name').val('');
            $('#last_name').val('');
            $('#email').val('');
            $('#mobile_number').val('');
        }
    });
});


$(document).ready(function () {
    $('#signup_wrapper').hide()
    // Get the current page's URL
    var currentPageURL = window.location.href;

    // Loop through the menu items and compare their href attributes to the current URL
    $('#navbar li a').each(function () {
        var menuItemURL = $(this).attr('href');
        if (currentPageURL.includes(menuItemURL)) {
            // If the current URL includes the menu item's URL, add the 'active' class
            $(this).closest('li a').addClass('active');
        }
    });

    $('#signup').on('click', function () {
        $('#login_wrapper').animate({
            opacity: 0, // Target opacity value (0 to 1 for fading in)
            top: '0', // Target left position (e.g., 100px from the left)
            // width: '0px', // Target width (e.g., 200px)
        }, 1000, function () {
            $('#login_wrapper').hide()
            $('#signup_wrapper').show().animate({
                opacity: 1, // Target opacity value (0 to 1 for fading in)
                top: '0',
                // width: '80%',
            }, 1100);
        });
    })
    $('#login_switch').on('click', function () {
        $('#signup_wrapper').animate({
            opacity: 0, // Target opacity value (0 to 1 for fading in)
            // width: '0',
        }, 1500, function () {
            $('#signup_wrapper').hide()
            $('#login_wrapper').show().animate({
                opacity: 1, // Target opacity value (0 to 1 for fading in)
                bottom: '0',
                // width: '80%',
            }, 1000);
        });
    })

});
// --------------------------------------------------------
//                  END LOGIN & SIGNUP JS
// --------------------------------------------------------



// --------- First Name on Signup -------------------
function validateSignupName(input) {
    // Trim leading and trailing spaces first
    input.value = input.value.trim();

    // Check if there are any invalid characters
    const invalidPattern = /[^a-zA-Z]/g;
    if (invalidPattern.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Input!',
            text: 'Only alphabetic characters are allowed, and no spaces!',
        });
        // Remove all invalid characters
        input.value = input.value.replace(invalidPattern, '');
    }

    // Capitalize the first letter and make the rest lowercase
    if (input.value.length > 0) {
        input.value = input.value.charAt(0).toUpperCase() + input.value.slice(1).toLowerCase();
    }
}
// ------------------------------------------------------



// --------- Mobile Number on Signup -------------------
function validateMobileNumber(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Limit the input to 10 digits
    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }

    // Check if the mobile number is exactly 10 digits long
    if (input.value.length === 10) {
        // Ensure the number starts with 7, 8, or 9
        if (!/^[789]/.test(input.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Mobile Number!',
                text: 'A valid mobile number must start with 7, 8, or 9.'
            });
            input.value = ''; // Clear the input
        }
    }
    // Check if the mobile number entered is less than 10 digits
    else if (input.value.length < 10) {
          Swal.fire({
              icon: 'error',
              title: 'Invalid Mobile Number!',
              text: 'Please enter 10 digit mobile number.'
          });
          input.value = ''; // Clear the input
    }
  }
// -------------------------------------------------------


// --------- Email on Signup -------------------
function validateEmailInput(input) {
    // Remove leading and trailing spaces
    input.value = input.value.trim();

    // Regular expression for a valid email format
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

    // Check if the input value matches the email pattern
    if (input.value && !emailPattern.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Email Address!',
            text: 'Please enter a valid email address.',
        });
        input.value = ''; // Clear the input if it's invalid
    }
}
// -------------------------------------------------------


// For Validating Password and Confirm Password in Sign_up Form
function validatePasswords() {
    const password = $('#password').val();
    const confirmPassword = $('#confirm_password').val();

    // Updated Regex for password validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;

    // Stage 1: Check password complexity
    if (password && !passwordRegex.test(password)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Password!',
            text: 'Password must have 8-20 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character.',
        });
        $('#password').val('');
        $('#confirm_password').val('');
        return false;  // Stop execution if password is invalid
    }

    // Stage 2: Check if passwords match
    if (password && confirmPassword && password !== confirmPassword) {
        Swal.fire({
            icon: 'error',
            title: 'Password Mismatch!',
            text: 'Password and Confirm Password do not match.',
        });
        $('#confirm_password').val('');  // Clear the confirm password field
        return false;  // Stop execution if passwords do not match
    }

    return true;  // Both password and confirm password are valid and match
}