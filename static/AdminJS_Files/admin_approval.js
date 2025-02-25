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
                                     <button class="btn btn-success btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModal${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModal${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>

                            <div class="modal fade" id="acceptModal${index + 1}" tabindex="-1" aria-labelledby="acceptModalLabel${index + 1}" style="display: none;">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="acceptModalLabel${index + 1}">Accept Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/accept_at_level_1" id="acceptForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="accept" value="accept">
                                                <p style="word-wrap: break-word;">
                                                    Please make sure you want to <span class="text-success fw-bold">accept</span> the following candidate:
                                                    <br> <strong>Name:</strong> ${record.first_name} ${record.last_name}.
                                                    <br> <strong>Email:</strong> ${record.email}
                                                    <br><br>
                                                    After you accept the applicant this applicant will be pending <br> review on the next stage.
                                                </p>
                                                <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>


                            <div class="modal fade" id="rejectModal${index + 1}" tabindex="-1" aria-labelledby="rejectModalLabel${index + 1}">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="rejectModalLabel${index + 1}">Reject Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/reject_at_level_1" id="rejectForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="reject" value="reject">
                                                <div class="mb-3">
                                                   <label for="rejectionReason" class="form-label">Rejection Reason</label>
                                                    <select name="rejectionReason" id="rejectionReason" class="form-select">
                                                        <option value="" disabled>-- Select a Reason --</option>
                                                        <option value="Application is Incomplete">Application is Incomplete</option>
                                                        <option value="Age Criteria is not Met">Age Criteria is not Met</option>
                                                        <option value="Application Deadline Missed">Application Deadline Missed</option>
                                                        <option value="All Documents are not uploaded">All Documents are not uploaded</option>
                                                        <option value="Document not matched at Offline and Online Scrutiny">Document not matched at Offline and Online Scrutiny</option>
                                                        <option value="Insufficient Academic Merit">Insufficient Academic Merit</option>
                                                        <option value="Caste Certificate criteria not met">Caste Certificate criteria not met</option>
                                                        <option value="Income Certificate criteria not met">Income Certificate criteria not met</option>
                                                        <option value="Domicile Certificate criteria not met">Domicile Certificate criteria not met</option>
                                                        <option value="Validity Certificate criteria not met">Validity Certificate criteria not met</option>
                                                        <option value="Other">Other</option>
                                                    </select>
                                                </div>
                                                <button type="submit" class="btn btn-danger">Submit Rejection</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>
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

$('#acceptModal').on('show.bs.modal', function (event) {
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
                                    <button class="btn btn-success btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModalTwo${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModalTwo${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>

                            <div class="modal fade" id="acceptModalTwo${index + 1}" tabindex="-1" aria-labelledby="acceptModalLabel${index + 1}" style="display: none;">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="acceptModalLabel${index + 1}">Accept Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/accept_at_level_2" id="acceptForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="accept" value="accept">
                                                <p style="word-wrap: break-word;">
                                                    Please make sure you want to <span class="text-success fw-bold">accept</span> the following candidate:
                                                    <br> <strong>Name:</strong> ${record.first_name} ${record.last_name}.
                                                    <br> <strong>Email:</strong> ${record.email}
                                                    <br><br>
                                                    After you accept the applicant this applicant will be pending <br> review on the next stage.
                                                </p>
                                                <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>


                            <div class="modal fade" id="rejectModalTwo${index + 1}" tabindex="-1" aria-labelledby="rejectModalLabel${index + 1}">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="rejectModalLabel${index + 1}">Reject Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/reject_at_level_2" id="rejectForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="reject" value="reject">
                                                <div class="mb-3">
                                                   <label for="rejectionReason" class="form-label">Rejection Reason</label>
                                                    <select name="rejectionReason" id="rejectionReason" class="form-select">
                                                        <option value="" disabled>-- Select a Reason --</option>
                                                        <option value="Application is Incomplete">Application is Incomplete</option>
                                                        <option value="Age Criteria is not Met">Age Criteria is not Met</option>
                                                        <option value="Application Deadline Missed">Application Deadline Missed</option>
                                                        <option value="All Documents are not uploaded">All Documents are not uploaded</option>
                                                        <option value="Document not matched at Offline and Online Scrutiny">Document not matched at Offline and Online Scrutiny</option>
                                                        <option value="Insufficient Academic Merit">Insufficient Academic Merit</option>
                                                        <option value="Caste Certificate criteria not met">Caste Certificate criteria not met</option>
                                                        <option value="Income Certificate criteria not met">Income Certificate criteria not met</option>
                                                        <option value="Domicile Certificate criteria not met">Domicile Certificate criteria not met</option>
                                                        <option value="Validity Certificate criteria not met">Validity Certificate criteria not met</option>
                                                        <option value="Other">Other</option>
                                                    </select>
                                                </div>
                                                <button type="submit" class="btn btn-danger">Submit Rejection</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>

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
                                    <button class="btn btn-success btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#acceptModalThree${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top" data-bs-original-title="Accept Applicant"><i class="mdi mdi-check-all"></i></button>
                                    <button class="btn btn-danger btn-sm tooltip-trigger" value="${record.applicant_id}" type="button" data-bs-toggle="modal" data-bs-target="#rejectModalThree${index + 1}" data-applicant-id="${record.applicant_id}" data-bs-placement="top"data-bs-original-title="Reject Applicant"><i class="mdi mdi-close-octagon"></i></button>
                                ` : ''}
                                <a href="/view_candidate/${record.id}" class="btn btn-info btn-sm btn-rounded tooltip-trigger" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-original-title="View Form"><i class="mdi mdi-eye-circle"></i></a>
                            </form>

                            <div class="modal fade" id="acceptModalThree${index + 1}" tabindex="-1" aria-labelledby="acceptModalLabel${index + 1}" style="display: none;">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="acceptModalLabel${index + 1}">Accept Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/accept_at_level_3" id="acceptForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="accept" value="accept">
                                                <p style="word-wrap: break-word;">
                                                    Please make sure you want to <span class="text-success fw-bold">accept</span> the following candidate:
                                                    <br> <strong>Name:</strong> ${record.first_name} ${record.last_name}.
                                                    <br> <strong>Email:</strong> ${record.email}
                                                    <br><br>
                                                    After you accept the applicant, this applicant will be given/accepted <br> for Fellowship for the year <span class="badge bg-warning text-dark fw-bold">${record.fellowship_application_year}</span>.
                                                </p>
                                                <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>


                            <div class="modal fade" id="rejectModalThree${index + 1}" tabindex="-1" aria-labelledby="rejectModalLabel${index + 1}">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h5 class="modal-title" id="rejectModalLabel${index + 1}">Reject Applicant</h5>
                                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <form action="/reject_at_level_3" id="rejectForm${index + 1}" method="POST">
                                                <input type="hidden" name="applicant_id" value="${record.applicant_id}">
                                                <input type="hidden" name="reject" value="reject">
                                                <div class="mb-3">
                                                   <label for="rejectionReason" class="form-label">Rejection Reason</label>
                                                    <select name="rejectionReason" id="rejectionReason" class="form-select">
                                                        <option value="" disabled>-- Select a Reason --</option>
                                                        <option value="Application is Incomplete">Application is Incomplete</option>
                                                        <option value="Age Criteria is not Met">Age Criteria is not Met</option>
                                                        <option value="Application Deadline Missed">Application Deadline Missed</option>
                                                        <option value="All Documents are not uploaded">All Documents are not uploaded</option>
                                                        <option value="Document not matched at Offline and Online Scrutiny">Document not matched at Offline and Online Scrutiny</option>
                                                        <option value="Insufficient Academic Merit">Insufficient Academic Merit</option>
                                                        <option value="Caste Certificate criteria not met">Caste Certificate criteria not met</option>
                                                        <option value="Income Certificate criteria not met">Income Certificate criteria not met</option>
                                                        <option value="Domicile Certificate criteria not met">Domicile Certificate criteria not met</option>
                                                        <option value="Validity Certificate criteria not met">Validity Certificate criteria not met</option>
                                                        <option value="Other">Other</option>
                                                    </select>
                                                </div>
                                                <button type="submit" class="btn btn-danger">Submit Rejection</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>
                            </div>

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

// -----------------------------------------------------------------------


// ----------------------------------------------
// ------ START
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#accepted_candidate_year').change(function () {
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
                    $.each(response.accepted_candidates, function (index, record) {  // Use $.each for cleaner iteration
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
                            record.phd_registration_date, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            scrutinyStatusLabel,
                            finalApprovalLabel
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

$('#acceptModal').on('show.bs.modal', function (event) {
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


// ----------------------------------------------
// ------ START
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#rejected_candidate_year').change(function () {
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
                    $.each(response.rejected_candidates, function (index, record) {  // Use $.each for cleaner iteration
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';
                        var rejectedLabel = '';

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

                        switch (record.rejected_at_level) {
                            case 'preliminary':
                                rejectedLabel = '<span class="text-danger text-capitalize">Preliminary Review</span>';
                                break;
                            case 'scrutiny_status':
                                rejectedLabel = '<span class="text-danger text-capitalize">Scrutiny Status</span>';
                                break;
                            case 'final_approval':
                                rejectedLabel = '<span class="text-danger text-capitalize">Final Approval</span>';
                                break;
                            default:
                                rejectedLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var rowData = [ // Prepare data for DataTables
                            index + 1, // Serial number
                            record.applicant_id,
                            record.first_name + ' ' + record.last_name,
                            record.email,
                            record.phd_registration_date, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            scrutinyStatusLabel,
                            finalApprovalLabel,
                            rejectedLabel
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
// --------------------------------------------------------------------
// END the Dynamic year wise list for approval level one



// ----------------------------------------------
// ------ START
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#pending_candidate_year').change(function () {
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
                    $.each(response.pending_candidates, function (index, record) {  // Use $.each for cleaner iteration
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
                            record.first_name + ' ' + record.last_name,
                            record.email,
                            record.phd_registration_date, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            scrutinyStatusLabel,
                            finalApprovalLabel

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
// --------------------------------------------------------------------
// END the Dynamic year wise list for approval level one



// ----------------------------------------------
// ------ START
$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();

    $('#disabled_candidate_year').change(function () {
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
                    $.each(response.disabled_candidates, function (index, record) {  // Use $.each for cleaner iteration
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
                            record.first_name + ' ' + record.last_name,
                            record.email,
                            record.phd_registration_date, // Make sure this key exists in your JSON
                            record.fellowship_application_year, // Make sure this key exists in your JSON
                            record.disability, // Make sure this key exists in your JSON
                            record.type_of_disability, // Make sure this key exists in your JSON
                            // Make sure this key exists in your JSON
                            statusLabel,
                            // Build the action HTML – use a template literal for cleaner code
                            scrutinyStatusLabel,
                            finalApprovalLabel

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
// --------------------------------------------------------------------
// END the Dynamic year wise list for approval level one


$(document).ready(function () {
    var dataTable = $('.datatable').DataTable();
    const yearSelector = $('#paymentYearSelector');
    const quarterSelector = $('#quarterSelector');

    function fetchData() {
        var selectedYear = yearSelector.val();
        var selectedQuarter = quarterSelector.val();

        if (selectedYear && selectedQuarter) {
            $.ajax({
                url: '/get_payment_sheet_data',
                type: 'GET',
                data: { year: selectedYear, quarter: selectedQuarter },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (response) {
                    dataTable.clear().draw();

                    $.each(response.hod_payment_data, function (index, record) { // Change to hod_payment_data to match your flask endpoint.
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)

                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.date,
                            record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<a class="btn btn-dark btn-sm" href="#"><i class="mdi mdi-eye text-white"></i></a>'
                        ];

                        dataTable.row.add(rowData);
                    });

                    dataTable.draw();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText);
                    alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    }

    yearSelector.change(fetchData);
    quarterSelector.change(fetchData);
});

// Get the year dropdown and the title element
const yearDropdown = document.getElementById('paymentYearSelector');
const paymentSheetTitle = document.getElementById('paymentSheetTitle');
const quarter = document.getElementById('quarterSelector');

// Function to update the title
function updateTitle() {
  const selectedYear = yearDropdown.value;
  const selectedQuarter = quarter.value;
    if (selectedYear) {
      const yearNumber = parseInt(selectedYear); // Convert to number
      if (!isNaN(yearNumber)) { //check if yearNumber is a number.
        val = 'BANRF ' + selectedYear + '-' + (yearNumber + 1);
      } else {
        val = "Invalid year";
      }

    } else {
        val = "Please select a year";
    }
  paymentSheetTitle.innerHTML = `Payment Sheet of <span style="font-weight: bold; color: blue;">${selectedQuarter}</span> for <span style="font-weight: bold; color: red;">${val}</span>`;
}

// Add event listeners to both dropdowns
yearDropdown.addEventListener('change', updateTitle);
quarter.addEventListener('change', updateTitle);

//Initial call to update title.
updateTitle();