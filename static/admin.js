// ----------------------------------------------
// ------ This code is for Send Bulk Emails -----
// Update preview as the user types
$('#subject').on('input', function () {
    $('.subject_text').html($(this).val())
})

$('#body').on('input', function () {
    $('.msg_text').html($(this).val())
})

$(document).ready(function () {
    // Attach a submit event handler to the form
    $('#emailForm').submit(function (event) {
        event.preventDefault();  // Prevent the form from submitting normally

        // Use AJAX to submit the form data and update the textarea
        $.ajax({
            type: 'POST',
            url: '/sendbulkEmails',
            data: $(this).serialize(),
            success: function (data) {
                // Update the textarea if email_list is defined
                if (data.email_list) {
                    $('#emailRecipients').val(data.email_list.join(', '));
                } else {
                    $('#emailRecipients').val('No emails found.');
                }
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    });
});

// Function to handle button click events
$(document).ready(function() {
    $('.export-excel').click(function(event) {
      event.preventDefault();
      // Check if the user has read-only access
      var hasReadOnlyAccess = true; // Replace this with your logic to determine read-only access
      if (hasReadOnlyAccess) {
        // Show SweetAlert modal
        Swal.fire({
          icon: 'warning',
          title: 'Read Only Access',
          text: 'Please contact the administrator to request Execution Access, as your current access level is Read Only.',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'OK'
        });
      } else {
        // Continue with button action if user has appropriate access
        // You can add your export or send email logic here
      }
    });
});
// ----------------------------------------------
// ------ End Code for Send Bulk Emails -----


// ---------------------- Start Selected Year on Admin Dashboard --------------
// Event listener to update the dashboard data based on selected year
$("#yearSelector").on("change", function () {
    const selectedYear = $(this).val();

    // Make an AJAX request to get the data for the selected year
    $.ajax({
        url: `/get_year_count?year=${selectedYear}`,
        method: "GET",
        dataType: "json",
        success: function (data) {
            console.log("Response data:", data);

            // Update the dashboard with the new data
            $("#total_appl_count").text(data.total_appl_count);
            $("#completed_form_count").text(data.completed_form_count);
            $("#incomplete_form_count").text(data.incomplete_form_count);
            $("#accepted_appl_count").text(data.accepted_appl_count);
            $("#rejected_appl_count").text(data.rejected_appl_count);
            $("#maleCount").text(data.male_count);
            $("#femaleCount").text(data.female_count);
            $("#disabled").text(data.disabled_count);
            $("#not_disabled").text(data.not_disabled_count);
            $("#science").text(data.faculty_counts.science);
            $("#arts").text(data.faculty_counts.arts);
            $("#commerce").text(data.faculty_counts.commerce);
            $("#other").text(data.faculty_counts.other);

            // Update the year in multiple places
            const yearChange = $("#yearSelector option:selected").text();
            $(".yearChange").each(function () {
                $(this).text(yearChange);
            });
        },
        error: function (error) {
            console.error("Error fetching data:", error);
            alert("Failed to load the data for the selected year.");
        },
    });
});


// ---------------------- END Selected Year on Admin Dashboard --------------


// ----------------------------------------------
// ------ This code is for Student Manage Dashboard Page -----
// Function to handle button click events
$(document).ready(function() {
    $('.export-excel').click(function(event) {
      event.preventDefault();
      // Check if the user has read-only access
      var hasReadOnlyAccess = true; // Replace this with your logic to determine read-only access
      if (hasReadOnlyAccess) {
        // Show SweetAlert modal
        Swal.fire({
          icon: 'warning',
          title: 'Read Only Access',
          text: 'Please contact the administrator to request Execution Access, as your current access level is Read Only.',
          confirmButtonColor: '#3085d6',
          confirmButtonText: 'OK'
        });
      } else {
        // Continue with button action if user has appropriate access
        // You can add your export or send email logic here
      }
    });
});
// ----------------------------------------------
// ------ END code is for Student Manage Dashboard Page -----

// ----------------------------------------------
// ------ Start Code for Total Application Report Page -----

$(document).ready(function () {
    /*
      This ID and Ajax Call is written for the functionality which is in:
      "/templates/AdminPages/DashboardCountReports/total_application_report.html"
      This code is responsible for handling the dynamic fetching of application report data based on the selected year.
      It utilizes DataTables with row selection.
      The AJAX call updates the DataTable based on the selected year and populates the table with new data.
      The route will be found in: "PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
    */
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#select_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/total_application_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});

$('#export-to-excel-total').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/total_application_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#select_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Total Application Report Page -----


// ----------------------------------------------
// ------ Start Code for Completed Form Report Page -----

$(document).ready(function () {
    /*
      Path to HTML: "/templates/AdminPages/DashboardCountReports/incompleted_form.html"
      Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
      This code is responsible for handling the dynamic fetching of application report data based on the selected year.
      It utilizes DataTables with row selection.
      The AJAX call updates the DataTable based on the selected year and populates the table with new data.
    */
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#selected_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/completed_form',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});

$('#export-to-excel').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/completed_form.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#selected_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Completed Form Report Page -----



// ----------------------------------------------
// ------ Start Code for IN Completed Form Report Page -----

$(document).ready(function () {
    /*
      Path to HTML: "/templates/AdminPages/DashboardCountReports/incompleted_form.html"
      Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
      This code is responsible for handling the dynamic fetching of application report data based on the selected year.
      It utilizes DataTables with row selection.
      The AJAX call updates the DataTable based on the selected year and populates the table with new data.
    */
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#selectedd_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/incompleted_form',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});


$('#export-to-excel-incomplete').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/incompleted_form.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#selectedd_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Incompleted Form Report Page -----


// ----------------------------------------------
// ------ Start Code for Accepted Applications Report Page -----

$(document).ready(function () {
    /*
      Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
      Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
      This code is responsible for handling the dynamic fetching of application report data based on the selected year.
      It utilizes DataTables with row selection.
      The AJAX call updates the DataTable based on the selected year and populates the table with new data.
    */
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#selectedd_yearr').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/total_accepted_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});

$('#export-to-excel-accepted').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/total_accepted_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#selectedd_yearr').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Accepted Application Report Page -----


// ----------------------------------------------
// ------ Start Code for Rejected Applications Report Page -----

$(document).ready(function () {
    /*
      Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
      Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
      This code is responsible for handling the dynamic fetching of application report data based on the selected year.
      It utilizes DataTables with row selection.
      The AJAX call updates the DataTable based on the selected year and populates the table with new data.
    */
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#selectedd_yearrr').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/total_rejected_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});

$('#export-to-excel-rejected').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/total_rejected_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#selectedd_yearrr').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Rejected Application Report Page -----


// ----------------------------------------------
// ------ Start Code for Male Report Page -----
/*
  Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
  Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
  This code is responsible for handling the dynamic fetching of application report data based on the selected year.
  It utilizes DataTables with row selection.
  The AJAX call updates the DataTable based on the selected year and populates the table with new data.
*/
$(document).ready(function () {
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#male_select_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/male_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.gender}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});

$('#export-to-excel-male').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/male_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#male_select_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Male Application Report Page -----



// ----------------------------------------------
// ------ Start Code for Female Report Page -----
/*
  Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
  Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
  This code is responsible for handling the dynamic fetching of application report data based on the selected year.
  It utilizes DataTables with row selection.
  The AJAX call updates the DataTable based on the selected year and populates the table with new data.
*/
$(document).ready(function () {
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#female_select_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/female_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.gender}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});
$('#export-to-excel-female').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/male_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#female_select_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Rejected Application Report Page -----


// ----------------------------------------------
// ------ Start Code for Disability Report Page -----
/*
  Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
  Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
  This code is responsible for handling the dynamic fetching of application report data based on the selected year.
  It utilizes DataTables with row selection.
  The AJAX call updates the DataTable based on the selected year and populates the table with new data.
*/
$(document).ready(function () {
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#disability_select_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/disabled_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.disability}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});
$('#export-to-excel-disabled').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/disabled_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#disability_select_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Disability Report Page -----


// ----------------------------------------------
// ------ Start Code for Not Disability Report Page -----
/*
  Path to HTML: "/templates/AdminPages/DashboardCountReports/total_accepted_report.html"
  Path to Python Route: "/PythonFiles/AdminPages/Dashboard/admin_dashboard.py"
  This code is responsible for handling the dynamic fetching of application report data based on the selected year.
  It utilizes DataTables with row selection.
  The AJAX call updates the DataTable based on the selected year and populates the table with new data.
*/
$(document).ready(function () {
    // Initialize the DataTable
    var dataTable = $('.datatable').DataTable();

    // Listen for changes in the year selector
    $('#not_disability_select_year').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/not_disabled_report',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Destroy the existing DataTable
                    dataTable.destroy();

                    // Clear the table body
                    $('.datatable tbody').empty();

                    // Populate the table with the new data
                    response.forEach(function (record) {
                        var statusLabel = '';
                        if (record.final_approval === 'accepted') {
                            statusLabel = '<label class="badge badge-gradient-success text-dark">Accepted</label>';
                        } else if (record.final_approval === 'rejected') {
                            statusLabel = '<label class="badge badge-gradient-danger text-dark">Rejected</label>';
                        } else if (record.final_approval === 'pending') {
                            statusLabel = '<label class="badge badge-gradient-warning text-dark">Pending</label>';
                        } else {
                            statusLabel = '<label>N/A</label>';
                        }

                        $('.datatable tbody').append(`
                            <tr>
                                <td>${record.applicant_id}</td>
                                <td>${record.first_name}</td>
                                <td>${record.last_name}</td>
                                <td>${record.disability}</td>
                                <td>${record.email}</td>
                                <td>${record.application_date}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/viewform/${record.id}" class="btn btn-primary btn-sm"
                                       data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form">
                                        <i class="mdi mdi-eye text-dark fw-bold"></i>
                                    </a>
                                </td>
                            </tr>
                        `);
                    });

                    // Reinitialize the DataTable with the updated data
                    dataTable = $('.datatable').DataTable();
                },
                error: function () {
                    alert('Failed to fetch data for the selected year. Please try again.');
                }
            });
        }
    });
});
$('#export-to-excel-not-disabled').on('click', function () {
    /*
        Go to this path: templates/AdminPages/DashboardCountReports/disabled_report.html
        On line 35, the ID is mentioned of the export to excel and the select_year id is on line 19.
        These ID's are used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/Dashboard/admin_dashboard.py on LINE 498.
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#not_disability_select_year').val();
    console.log('Selected year:', selectedYear);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2023
    if (selectedYear === '') {
        selectedYear = 2023;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Not Disabled Report Page -----


