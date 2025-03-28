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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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
                                <td>${record.phd_registration_year}</td>
                                <td>${statusLabel}</td>
                                <td>
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm"
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


//----------------------------------------------------------------
//-------------Validations for Add Admin in HoD Login-------------

function validateName(input) {
    // Remove leading spaces
    input.value = input.value.replace(/^\s+/g, '');

    // Remove non-alphabetic characters (except spaces)
    input.value = input.value.replace(/[^a-zA-Z\s]/g, '');

    // Ensure the first letter is capitalized and the rest are lowercase
    input.value = input.value
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
        .join(' ');

    const englishOnlyPattern = /^[A-Za-z0-9.,'"\s\-()]*$/;

    if (!englishOnlyPattern.test(input.value)) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Langauge Detected!',
            text: 'Please enter the Topic of Ph.D in English only. If the topic is in Marathi, Please translate and then enter the text.'
        });
        $(this).val('')
        input.value = input.value.replace(/[^A-Za-z0-9.,'"\s\-()]/g, ''); // Remove invalid characters
    }
}

// --------- Mobile Number on Section 1 -------------------
function validateMobileNumber(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Allow integers only upto 10 digits
    if (input.value.length > 10) {
        input.value = input.value.slice(0, 10);
    }
    // Mobile Number should start with 7, 8, or 9.
    if (input.value.length === 10) {
        if (!/^[789]/.test(input.value)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Number Detected!',
                text: 'Mobile Number should start with 7, 8, or 9.'
            });
            input.value = ''; 
        }
    } else if (input.value.length > 0 && input.value.length < 10) {
        // If digits are less than 10
        Swal.fire({
            icon: 'error',
            title: 'Incomplete Number!',
            text: 'Mobile Number must be exactly 10 digits.'
        });
        input.value = ''; 
    }
}

function validateAge(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

    // Allow integers only upto 10 digits
    if (input.value.length > 2) {
        input.value = input.value.slice(0, 2);
    }

    if (input.value === '0' || input.value === '00') {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Age!',
            text: 'Please enter correct age.'
        });
        input.value = ''; 
    } 
}

function ValidateDoB(input) {
    const dobInput = input.value; // Get the value from the input field

    // Ensure the input has a complete date in the format YYYY-MM-DD
    if (!dobInput || dobInput.length < 10) {
        Swal.fire({
            icon: 'error',
            title: 'Incomplete Date!',
            text: 'Please enter Complete Date of Birth.'
        });
        input.value = ''; // Clear the input if the date is invalid
        return; // Exit the function
    }

    // Validate the entered date
    const enteredDate = new Date(dobInput);
    if (isNaN(enteredDate.getTime())) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Date Format!',
            text: 'Please enter a valid date in the format YYYY-MM-DD.'
        });
        input.value = ''; // Clear the input if the date is invalid
        return; // Exit the function
    }
    // Check if the entered date is not in the future
    const today = new Date();
    if (enteredDate > today) {
        Swal.fire({
            icon: 'error',
            title: 'Invalid Date!',
            text: 'Date cannot be greater than today\'s date.'
        });
        input.value = ''; // Clear the input if the date is invalid
        return; // Exit the function
    }
}

// For Validating Password and Confirm Password in Add Admin Form
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
// ----------------------END Add Admin Validations---------------------------------
// --------------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".editAdminBtn").forEach(button => {
        button.addEventListener("click", function() {
            // Populate form fields
            document.getElementById("edit_id").value = this.dataset.id;
            document.getElementById("edit_first_name").value = this.dataset.first_name;
            document.getElementById("edit_middle_name").value = this.dataset.middle_name;
            document.getElementById("edit_surname").value = this.dataset.surname;
            document.getElementById("edit_email").value = this.dataset.email;
            document.getElementById("edit_username").value = this.dataset.username;
            document.getElementById("edit_role").value = this.dataset.role;
            document.getElementById("edit_year").value = this.dataset.year;
            document.getElementById("edit_mobile_number").value = this.dataset.mobile_number;

            // Set form action dynamically
            document.querySelector("#editAdminModal form").action = "/edit_admin/" + this.dataset.id;
        });
    });
});


function validateAmount(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 10 digits
        if (input.value.length > 10) {
            input.value = input.value.slice(0, 10);
        }     

        if (input.value === '0') {
            input.value = '';
        }  
    }

function validateHRArate(input) {
    // Remove any non-numeric characters
    input.value = input.value.replace(/[^0-9]/g, '');

        // Limit the input to 2 digits
        if (input.value.length > 2) {
            input.value = input.value.slice(0, 2);
        }     

        if (input.value === '0') {
            input.value = '';
        }  
    }    

    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll(".editHRABtn").forEach(button => {
            button.addEventListener("click", function() {
                // Populate form fields
                console.log("Dataset values:", this.dataset); 
                
                document.getElementById("edit_id").value = this.dataset.id;
                document.getElementById("edit_for_year").value = this.dataset.for_year;
                document.getElementById("edit_date_criteria").value = this.dataset.date_criteria;
                document.getElementById("edit_fellowship_amount").value = this.dataset.fellowship_amount;
                document.getElementById("edit_less_greater_than").value = this.dataset.less_greater_than;
                document.getElementById("edit_jrf_srf").value = this.dataset.jrf_srf;
                document.getElementById("edit_X_rate").value = this.dataset.x_rate;
                document.getElementById("edit_Y_rate").value = this.dataset.y_rate;
                document.getElementById("edit_Z_rate").value = this.dataset.z_rate;
                document.getElementById("edit_contingency_other").value = this.dataset.contingency_other;
                document.getElementById("edit_contingency_science").value = this.dataset.contingency_science;
                document.getElementById("edit_disability").value = this.dataset.disability;
    
                // Set form action dynamically
                document.querySelector("#editHRAModal form").action = "/edit_hra_rate/" + this.dataset.id;
            });
        });
    });


// ----------------------------------------------
// ------ Start Code for Pending Applications Report Page -----

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
    $('#selectedd_yearrrs').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            // Make an AJAX GET request
            $.ajax({
                url: '/total_pending_report',
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
                                    <a href="/view_candidate/${record.id}" class="btn btn-primary btn-sm" target="_blank"
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

$('#export-to-excel-pending').on('click', function () {
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
        selectedYear = 2024;
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_to_excel?year=${selectedYear}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});
// ----------------------------------------------
// ------ END Code for Pending Application Report Page -----    


$('#export_payment_sheet').on('click', function () {
    /*
        Go to this path: templates/AdminPages/PaymentSheet/payment_sheet.html
        The "export_payment_sheet" ID is mentioned of the export to excel.
        This ID is used to fetch data and hit the export to excel link.
        Python code path: /PythonFiles/AdminPages/PaymentSheet/payment_sheet.py
    */
    // Get the selected year from the dropdown
    let selectedYear = $('#paymentYearSelector').val();
    console.log('Selected year:', selectedYear);
    let selectedQuarter= $('#quarterSelector').val();
    console.log('Selected Qaurter:', selectedQuarter);
    const formType = $(this).data('form-type');  // Get the form type (e.g., "completed_form")

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    // If no quarter is selected, then set default to Quarter 1
    if (selectedQuarter === '') {
        selectedQuarter = 'Quarter 1';
    }
    // Set the href of the export link dynamically with the selected year
    // Dynamically build the export link using the selected year and form type
    const exportHref = `/export_payment_sheet?year=${selectedYear}&quarter=${selectedQuarter}&form_type=${formType}`;

    // Set the href of the export link dynamically
    $(this).attr('href', exportHref);
});

$('#export_payment_sheet_pdf').on('click', function () {
    let selectedYear = $('#paymentYearSelector').val();
    let selectedQuarter = $('#quarterSelector').val();

    if (selectedYear === '') {
        selectedYear = 2024;
    }

    if (selectedQuarter === '') {
        selectedQuarter = 'Quarter 1';
    }

    const iframeSrc = `/generate_pdf?year=${selectedYear}&quarter=${selectedQuarter}`;
    $('#pdfIframe').attr('src', iframeSrc);
});

// Export Preliminary Review - Level One for Admin and HOD
$('#export_level_one').on('click', function () {
    let selectedYear = $('#approval_year_selector').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_level_one_applications?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Eligibility Check - Level Two for Admin and HOD
$('#export_level_two').on('click', function () {
    let selectedYear = $('#approval_year_selector_two').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_level_two_applications?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Final Approval - Level Three for Admin and HOD
$('#export_level_three').on('click', function () {
    let selectedYear = $('#approval_year_selector_three').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_level_three_admin?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Accepted Applications for Admin and HOD
$('#export_accepted_applications').on('click', function () {
    let selectedYear = $('#accepted_candidate_year').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_accpeted_candidates?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Rejected Approval for Admin and HOD
$('#export_rejected_applications').on('click', function () {
    let selectedYear = $('#rejected_candidate_year').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_rejected_candidates?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Pending Approval for Admin and HOD
$('#export_pending_applications').on('click', function () {
    let selectedYear = $('#pending_candidate_year').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_pending_candidates?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});

// Export Disabled Candidates for Admin and HOD
$('#export_disabled_applications').on('click', function () {
    let selectedYear = $('#disabled_candidate_year').val(); // Assuming the dropdown ID is approval_year_selector_two
    alert("The Year Selected is :" + selectedYear)

    // If no year is selected, default to 2024
    if (selectedYear === '') {
        selectedYear = 2024;
    }
    const exportHref = `/export_disabled_candidates?year=${selectedYear}`;

    $(this).attr('href', exportHref);
});
