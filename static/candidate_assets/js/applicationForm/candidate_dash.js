const researchPaperSelect = document.getElementById('research_paper_select');
const researchPaperUpload = document.getElementById('research_paper_upload');
const feedback_select = document.getElementById('feedback_select');
const write_feedback = document.getElementById('write_feedback');
const research_paper_file = document.getElementById('research_paper_file');
const write_feedback_here = document.getElementById('write_feedback_here');

researchPaperSelect.addEventListener('change', function() {
    if (this.value === 'Yes') {
        researchPaperUpload.style.display = 'block';
    } else {
        researchPaperUpload.style.display = 'none';
        research_paper_file.value = '';
    }
});

feedback_select.addEventListener('change', function() {
    if (this.value === 'Yes') {
        write_feedback.style.display = 'block';
    } else {
        write_feedback.style.display = 'none';
        write_feedback_here.value = '';
    }
});

// For Validating Password and Confirm Password in Sign_up Form
function validatePasswords() {
    const password = $('#new-password').val();
    const confirmPassword = $('#confirm-password').val();

    // Updated Regex for password validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$/;

    // Stage 1: Check password complexity
    if (password && !passwordRegex.test(password)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Password!',
            text: 'Password must have 8-20 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character.',
        });
        $('#new-password').val('');
        $('#confirm-password').val('');
        return false;  // Stop execution if password is invalid
    }

    // Stage 2: Check if passwords match
    if (password && confirmPassword && password !== confirmPassword) {
        Swal.fire({
            icon: 'error',
            title: 'Password Mismatch!',
            text: 'Password and Confirm Password do not match.',
        });
        $('#confirm-password').val('');  // Clear the confirm password field
        return false;  // Stop execution if passwords do not match
    }

    return true;  // Both password and confirm password are valid and match
}

    function checkCurrentPassword(e){
            const currentPassword = e.value;
            if (currentPassword) {
                $.ajax({
                    url: '/check-current-password',  // Corrected Flask API route
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({ password: currentPassword }),
                    success: function (response) {
                        if (!response.valid) {
                            Swal.fire({
                                icon: 'error',
                                title: 'Incorrect Password!',
                                text: response.message,
                            });
                            $('#current_password').val('');  // Clear the field
                        } else {
                            Swal.fire({
                                icon: 'success',
                                title: 'Password Verified!',
                                text: response.message,
                                timer: 2000
                            });
                        }
                    },
                    error: function () {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error!',
                            text: 'Something went wrong. Please try again.',
                        });
                    }
                });
            }
        };



