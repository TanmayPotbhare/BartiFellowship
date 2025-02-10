// ----------------------------------------------
// ------ START
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#approval_year_selector').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            $.ajax({
                url: '/get_approval_year',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Clear the DataTable (more efficient than destroy and re-create)
                    dataTable.clear().draw();

//                    response = JSON.parse(response)
                    // Add new data
                    $.each(response.admin_level_one_list, function (index, record) {  // Use $.each for cleaner iteration
                        var statusLabel = '';
                        switch (record.status) {
                            case 'accepted':
                                statusLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                statusLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                statusLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                statusLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var rowData = [ // Prepare data for DataTables
                            index + 1, // Serial number
                            record.applicant_id,
                            record.first_name + record.last_name,
                            record.email,
                            record.mobile_number, // Make sure this key exists in your JSON
                            record.phd_registration_date, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            `
                            <form method="POST">
                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                ${record.status === 'pending' ? `
                                    <button class="btn btn-success btn-sm tooltip-trigger open_modal" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModal" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModal" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>
                            `

                        ];

                        dataTable.row.add(rowData); // Add the row to DataTables
                    });

                   dataTable.draw(); // Redraw the table
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText); // Log the error for debugging
                    alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    });
});
$(document).on('click','.open_modal',function(){
alert('click')
$('#acceptModal').modal('show')
})
$(document).on('click','#acceptModal', function (event) {
    alert('HI');
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#acceptApplicantId').val(applicantId); // Use jQuery's .val() for setting value
});

$('#rejectModal').on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#rejectApplicantId').val(applicantId); // Use jQuery's .val()
});

// --------------------------------------------------------------------
// END the Dynamic year wise list for approval level one


// --------------------------------------------------------------------
// START the dynamic year wise list for approval level two
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#approval_year_selector_two').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            $.ajax({
                url: '/get_approval_year_two',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Clear the DataTable (more efficient than destroy and re-create)
                    dataTable.clear().draw();

//                    response = JSON.parse(response)
                    // Add new data
                    $.each(response.admin_level_two_list, function (index, record) {  // Use $.each for cleaner iteration
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';

                        switch (record.status) {
                            case 'accepted':
                                statusLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                statusLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                statusLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                statusLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        switch (record.scrutiny_status) {
                            case 'accepted':
                                scrutinyStatusLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                scrutinyStatusLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                scrutinyStatusLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                scrutinyStatusLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var rowData = [ // Prepare data for DataTables
                            index + 1, // Serial number
                            record.applicant_id,
                            record.first_name + record.last_name,
                            record.email,
                            record.mobile_number, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            scrutinyStatusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            `
                            <form method="POST">
                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                ${record.scrutiny_status === 'pending' ? `
                                    <button class="btn btn-success btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModalTwo" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModalTwo" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>
                            `

                        ];

                        dataTable.row.add(rowData); // Add the row to DataTables
                    });

                   dataTable.draw(); // Redraw the table
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText); // Log the error for debugging
                    alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    });
});

$('#acceptModalTwo').on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#acceptApplicantId').val(applicantId); // Use jQuery's .val() for setting value
});

$('#rejectModalTwo').on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#rejectApplicantId').val(applicantId); // Use jQuery's .val()
});
// -------------------------------------------------------------------
// END the Dynamic Year wise report for Level 2


// --------------------------------------------------------------------
// START the dynamic year wise list for approval level three
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#approval_year_selector_three').change(function () {
        var selectedYear = $(this).val();

        if (selectedYear) {
            $.ajax({
                url: '/get_approval_year_three',
                type: 'GET',
                data: { year: selectedYear },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' // Ensure the server recognizes it as an AJAX call
                },
                success: function (response) {
                    // Clear the DataTable (more efficient than destroy and re-create)
                    dataTable.clear().draw();

//                    response = JSON.parse(response)
                    // Add new data
                    $.each(response.admin_level_three_list, function (index, record) {  // Use $.each for cleaner iteration
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        switch (record.status) {
                            case 'accepted':
                                statusLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                statusLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                statusLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                statusLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        switch (record.scrutiny_status) {
                            case 'accepted':
                                scrutinyStatusLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                scrutinyStatusLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                scrutinyStatusLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                scrutinyStatusLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        switch (record.final_approval) {
                            case 'accepted':
                                finalApprovalLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted</span>';
                                break;
                            case 'rejected':
                                finalApprovalLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected</span>';
                                break;
                            case 'pending':
                                finalApprovalLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                finalApprovalLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var rowData = [ // Prepare data for DataTables
                            index + 1, // Serial number
                            record.applicant_id,
                            record.first_name + record.last_name,
                            record.email,
                            record.mobile_number, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            scrutinyStatusLabel,
                            finalApprovalLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            `
                            <form method="POST">
                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                ${record.final_approval === 'pending' ? `
                                    <button class="btn btn-success btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModalThree" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModalThree" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>
                            `

                        ];

                        dataTable.row.add(rowData); // Add the row to DataTables
                    });

                   dataTable.draw(); // Redraw the table
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText); // Log the error for debugging
                    alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    });
});

$('#acceptModalThree').on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#acceptApplicantId').val(applicantId); // Use jQuery's .val() for setting value
});

$('#rejectModalThree').on('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const applicantId = button.dataset.applicantId;
    $('#rejectApplicantId').val(applicantId); // Use jQuery's .val()
});
