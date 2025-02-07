
// ---------------- Section 5 Validation ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('.doc_language');
    const errorMessages = document.querySelectorAll('.fileError');

    fileInputs.forEach((fileInput, index) => {
        fileInput.addEventListener('change', function(event) {
            const file = fileInput.files[0];
            const fileName = file.name;
            const regex = /^[a-zA-Z0-9 _-]+\.pdf$/;

            if (!regex.test(fileName)) {
                errorMessages[index].textContent = 'File name must contain only English letters, numbers, spaces, underscores, or hyphens, and end with .pdf';
                fileInput.value = ''; // Clear the input
            } else {
                errorMessages[index].textContent = '';
            }
        });
    });
});




// ----------------------- Old User Preview Form ------------------------
$(document).ready(function () {
    $('#village').on('change', function () {
        let choice = $(this).val()
        if (choice == 'other') {
              $('#taluka').attr('disabled',false)
              $('#city').attr('disabled',false)
              $('#district').attr('disabled',false)
              $('#state').attr('disabled',false)
        }else{
            $('#taluka').attr('disabled',true)
              $('#city').attr('disabled',true)
              $('#district').attr('disabled',true)
              $('#state').attr('disabled',true)
        }
      })
    })


// ----------------- MY Profile Page -------------------------------
$(document).ready(function(){


    $('.validatepassword').on('blur', function(){
     var currentPassword = $('#currentPassword').val()
      var newPassword = $('#newPassword').val()
      var confirm_password = $('#confirm_password').val()
      if(currentPassword == newPassword && currentPassword != '' && newPassword != ''){
        Swal.fire({
            title: "Current Password and NewPassword cannot be the same",
            text: '',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
        $('#currentPassword').val('')
        $('#newPassword').val('')
      }

    })

    $('.confirmPass').on('blur',function(){
    var newPassword = $('#newPassword').val()
    var confirm_password = $('#confirm_password').val()
    if(newPassword != confirm_password && confirm_password != '' && newPassword != ''){
        Swal.fire({
            title: "New Password and Confirm Password should match",
            text: '',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
        $('#newPassword').val('')
        $('#confirm_password').val('')
      }
    }
    )

  })

  {% if flash_msg == 'success' %}

      $(document).ready(function () {
            Swal.fire({
              icon: "success",
              title: "Password Changed Successfully",
              text: `Please check your Email`,
            });
      })
  {% endif %}

  {% if flash_msg_profile == 'success' %}

  $(document).ready(function () {
        Swal.fire({
          icon: "success",
          title: "Looks Good!",
          text: `Changes saved Successfully`,
        });
  })
{% endif %}


