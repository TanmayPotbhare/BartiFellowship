// Accept image format only for input type file
$('.accept_img').on('input', function () {
    // Allowed file extensions
    var allowExtensions = ['jpg', 'jpeg', 'png'];

    // File size limits
    var minFileSize = 50 * 1024; // 50 KB
    var maxFileSize = 100 * 1024; // 100 KB

    // Get selected file
    var uploadFile = this.files[0];

    // English-only regex (allowing only alphabets, numbers, spaces, and specific punctuation marks)
    const englishOnlyPattern = /^[A-Za-z0-9.,'"\s\-()]*$/;

    if (uploadFile) {
        var fileName = uploadFile.name;
        var fileExtension = fileName.split('.').pop().toLowerCase();

        // Validate file extension
        if (allowExtensions.indexOf(fileExtension) === -1) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid File Type',
                text: 'Allowed file types are JPG, JPEG, and PNG.',
            });
            $(this).val(''); // Reset file input
            return;
        }

        // Validate file size
        if (uploadFile.size < minFileSize || uploadFile.size > maxFileSize) {
            Swal.fire({
                icon: 'warning',
                title: 'Invalid File Size',
                text: 'File size must be between 50KB and 100KB.',
            });
            $(this).val(''); // Reset file input
            return;
        }

        // If the file is an image, you may want to add logic here for extracting text via OCR (Optional).
        // For example, using an OCR library to extract text from the image.

        // Check if the filename is in English
        if (!englishOnlyPattern.test(fileName)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Language Detected',
                text: 'The file name contains invalid characters. Please use English letters and numbers only.',
            });
            $(this).val(''); // Reset file input
            return;
        }
    }
});
// --------------------------------------------------


// Accept pdf format only for input type file
$('.accept_pdf').on('change', function () {
    // File extension allowed on site
    var allowExtensions = ['pdf'];

    // Max file size is defined (250 KB)
    var maxFileSize = 250 * 1024;

    // English-only regex (allowing only alphabets, numbers, spaces, and specific punctuation marks)
    const englishOnlyPattern = /^[A-Za-z0-9.,'"\s\-()]*$/;

    // Get selected file
    var uploadFile = this.files[0];

    if (uploadFile) {
        var fileName = uploadFile.name;
        var fileExtension = fileName.split('.').pop().toLowerCase();

        if (allowExtensions.indexOf(fileExtension) === -1) {
            Swal.fire({
                icon: 'error',
                title: 'Sorry',
                text: 'Invalid file type. Allowed file types are PDF.'
            });
            $(this).val('')
        }

        if (uploadFile.size > maxFileSize) {
            Swal.fire({
                icon: 'warning',
                title: 'Sorry',
                text: 'File size exceeds the maximum allowed size of 250KB.',
            });
            $(this).val('')
        }

        // Check if the filename is in English
        if (!englishOnlyPattern.test(fileName)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Language Detected',
                text: 'The file name contains invalid characters. Please use English letters and numbers only.',
            });
            $(this).val(''); // Reset file input
            return;
        }
    }

})

     // Enable "View" button when an image file is selected
     function toggleViewImageButton(input, viewButtonId) {
        var viewButton = document.getElementById(viewButtonId);
        var file = input.files[0];

        if (file && file.type.startsWith('image/')) {
            viewButton.style.display = "inline-block"; // Show the "View" button
        } else {
            viewButton.style.display = "none"; // Hide if no valid file selected
        }
    }

    // Open the selected image in a new tab
    function openImage(fileInputId) {
        var fileInput = document.getElementById(fileInputId);
        if (fileInput.files[0]) {
            var fileURL = URL.createObjectURL(fileInput.files[0]);
            window.open(fileURL, '_blank'); // Open in a new tab
        }
    }

    // Enable "View Document" button when a PDF file is selected

    function toggleViewDocumentButton(input, viewButtonId) {
        var viewButton = document.getElementById(viewButtonId);
        var file = input.files[0];

        if (file && file.type === 'application/pdf') {
            viewButton.style.display = "inline-block"; // Show the "View" button
        } else {
            viewButton.style.display = "none"; // Hide if no valid file selected
        }
    }

    // Open the document (PDF) in a new tab when the "View Document" button is clicked
    function openDocument(fileInputId) {
        var fileInput = document.getElementById(fileInputId);
        var fileURL = URL.createObjectURL(fileInput.files[0]);
        window.open(fileURL, '_blank'); // Open in a new tab
    }
