$(document).ready(function () {
    // This JS is resposible for loading the Payment Sheet Records based on the options selected in Dropdown.
    var dataTable = $('.datatable').DataTable();
    const yearSelector = $('#paymentYearSelector');
    const quarterSelector = $('#quarterSelector');

    function fetchData() {
        // alert("Main Payment Sheet Data");
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

                    // alert("Main Year:" + selectedYear);
                    // alert("Main Quarter:" + selectedQuarter);
                    dataTable.clear().draw();

                    $.each(response.hod_payment_data, function (index, record) { // Change to hod_payment_data to match your flask endpoint.
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        function formatDate(dateString) {
                              const date = new Date(dateString);
                              const options = {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                              };
                              return date.toLocaleDateString('en-US', options).replace(/,/g, '');
                        }
                        const dateString = record.date; // Simply assign the value
                        const formattedDate = formatDate(dateString);

                        var jrf_srf = '';
                        switch (record.jrf_srf) {
                            case 'jrf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'jrf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'srf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_3':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            default:
                                jrf_srf = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var AdminLabel = '';
                        if (record.admin_action === null || record.admin_action === undefined) {
                            AdminLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.admin_action) {
                                case 'Approved by Admin':
                                    AdminLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                    break;
                                case 'Rejected by Admin':
                                    AdminLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                    break;
                                case 'On Hold by Admin':
                                    AdminLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                    break;
                                default:
                                    AdminLabel = '<span>N/A</span>';
                            }
                        }

                        var AdminButton = '';
                        switch (record.admin_approval) {
                            case 'accepted':
                                AdminButton = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                break;
                            case 'rejected':
                                AdminButton = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                break;
                            case 'hold':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                break;
                            case 'N/A':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                AdminButton = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var HODLabel = '';
                        if (record.hod_action === null || record.hod_action === undefined) {
                            HODLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.hod_action) {
                                case 'Approved by Head of Department':
                                    HODLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Head of Department</span>';
                                    break;
                                case 'Rejected by Head of Department':
                                    HODLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Head of Department</span>';
                                    break;
                                case 'On Hold by Head of Department':
                                    HODLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Head of Department</span>';
                                    break;
                                default:
                                    HODLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var AOLabel = '';
                        if (record.ao_action === null || record.ao_action === undefined) {
                            AOLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.ao_action) {
                                case 'Approved by Account Officer':
                                    AOLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Account Officer</span>';
                                    break;
                                case 'Rejected by Account Officer':
                                    AOLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Account Officer</span>';
                                    break;
                                case 'On Hold by Account Officer':
                                    AOLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Account Officer</span>';
                                    break;
                                default:
                                    AOLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var RegistrarLabel = '';
                        if (record.registrar_action === null || record.registrar_action === undefined) {
                            RegistrarLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.registrar_action) {
                                case 'Approved by Registrar':
                                    RegistrarLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Registrar</span>';
                                    break;
                                case 'Rejected by Registrar':
                                    RegistrarLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Registrar</span>';
                                    break;
                                case 'On Hold by Registrar':
                                    RegistrarLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Registrar</span>';
                                    break;
                                default:
                                    RegistrarLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }
                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)


                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.email,
                            '<strong>' + jrf_srf + '</strong>',
                            record.faculty,
                            formattedDate,
                            'BANRF - ' + record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            '<strong>' + record.total_months + '</strong>' + ' ' + 'Months',
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<strong>INR</strong>' + ' ' + record.total_fellowship,
                            record.hra_rate + ' ' + '<strong>%</strong>',
                            record.hra_amount,
                            record.hra_months,
                            '<strong>INR</strong>' + ' ' + record.total_hra_rate,
                            '<strong>INR</strong>' + ' ' + record.contingency,
                            '<strong>INR</strong>' + ' ' + record.pwd,
                            '<strong>INR</strong>' + ' ' + record.total,
                            '<span class="badge badge-primary bg-primary text-capitalize">' + record.city + '<span>',
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            AdminLabel,
                            HODLabel,
                            AOLabel,
                            RegistrarLabel,
                            `
                                <td>
                                    <form method="POST">
                                        <input type="hidden" name="sheet_id" value="${record.number}">
                                            <button class="btn btn-success btn-sm tooltip-trigger" type="button"
                                                data-bs-toggle="modal" data-bs-target="#acceptModal${record.number}"
                                                data-applicant-id="${record.number}" data-bs-placement="top"
                                                data-bs-original-title="Accept Sheet">
                                                <i class="mdi mdi-check-all"></i>
                                            </button>
                                            <button class="btn btn-danger btn-sm tooltip-trigger" type="button"
                                                data-bs-toggle="modal" data-bs-target="#rejectModal${record.number}"
                                                data-applicant-id="${record.number}" data-bs-placement="top"
                                                data-bs-original-title="Reject Sheet">
                                                <i class="mdi mdi-close-octagon"></i>
                                            </button>
                                            <button class="btn btn-warning btn-sm tooltip-trigger" type="button"
                                                data-bs-toggle="modal" data-bs-target="#holdModal${record.number}"
                                                data-applicant-id="${record.number}" data-bs-placement="top"
                                                data-bs-original-title="Hold Sheet">
                                                <i class="mdi mdi-close-octagon"></i>
                                            </button>
                                    </form>
                                </td>

                                <div class="modal fade" id="acceptModal${record.number}" tabindex="-1" aria-labelledby="acceptModalLabel" style="display: none;">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="acceptModalLabel${record.number}">Accept Applicant</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_accept_payment_sheet" id="acceptForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="accept" value="accept">
                                                    <p style="word-wrap: break-word;">
                                                        Please make sure you want to <span class="text-success fw-bold">Accept</span> the following Payment Sheet :
                                                        <br> <strong>Name:</strong> ${record.full_name}.
                                                        <br> <strong>Fellowship:</strong> ${record.jrf_srf}
                                                        <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                        <br><br>
                                                        After you accept the Payment Sheet,
                                                        <br> it will be passed on to HoD for further approval.
                                                    </p>
                                                    <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="modal fade" id="rejectModal${record.number}" tabindex="-1" aria-labelledby="rejectModalLabel">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="rejectModalLabel${record.number}">Reject Applicant</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_reject_payment_sheet" id="rejectForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="email" value="${record.email}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="reject" value="reject">

                                                        <p style="word-wrap: break-word;">
                                                            Please make sure you want to <span class="text-danger fw-bold">Reject</span> the following Payment Sheet :
                                                            <br> <strong>Name:</strong> ${record.full_name}.
                                                            <br> <strong>Fellowship:</strong> jrf_srf
                                                            <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                            <br><br>
                                                        </p>

                                                    <div class="mb-3">
                                                    <label for="rejectionReason" class="form-label">Rejection Reason</label>
                                                        <select name="rejectionReason" id="rejectionReason" class="form-select">
                                                            <option value="" selected>-- Select a Reason --</option>
                                                            <option value="Missing required documents">Missing required documents</option>
                                                            <option value="Progress Report not uploaded">Progress Report not uploaded</option>
                                                            <option value="Half Yearly Report not uploaded">Half Yearly Report not uploaded</option>
                                                            <option value="House Rent Allowance Report not uploaded">House Rent Allowance Report not uploaded</option>
                                                            <option value="Missing required documents">Missing required documents</option>
                                                            <option value="Expired documents">Expired documents</option>
                                                            <option value="The candidate is double beneficiary">The candidate is double beneficiary</option>
                                                            <option value="Providing inaccurate or falsified information in the application">Providing inaccurate or falsified information in the application</option>
                                                            <option value="Mismatched name on the bank account">Mismatched name on the bank account</option>
                                                            <option value="Payment was already issued">Payment was already issued</option>
                                                            <option value="Failure to submit required financial reports">Failure to submit required financial reports</option>
                                                            <option value="Failure to adhere to the fellowship's code of conduct">Failure to adhere to the fellowships code of conduct</option>
                                                            <option value="Cancellation or suspension of the fellowship program">Cancellation or suspension of the fellowship program</option>
                                                            <option value="Changes in funding priorities">Changes in funding priorities</option>
                                                        </select>
                                                    </div>
                                                    <button type="submit" class="btn btn-danger">Submit Rejection</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="modal fade" id="holdModal${record.number}" tabindex="-1" aria-labelledby="holdModalLabel">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="holdModalLabel${record.number}">Hold Payment Sheet</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_hold_payment_sheet" id="holdForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="hold" value="hold">

                                                        <p style="word-wrap: break-word;">
                                                            Please make sure you want to keep the Payment Sheet <span class="text-warning fw-bold">On Hold</span>:
                                                            <br> <strong>Name:</strong> ${record.full_name}.
                                                            <br> <strong>Fellowship:</strong> ${record.jrf_srf}
                                                            <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                            <br><br>
                                                        </p>

                                                    <div class="mb-3">
                                                    <label for="rejectionReason" class="form-label">On Hold Reason</label>
                                                        <select name="onHoldReason" id="onHoldReason" class="form-select">
                                                            <option value="" selected>-- Select a Reason --</option>
                                                            <option value="The candidate is double beneficiary">The candidate is double beneficiary</option>
                                                            <option value="Test1">Test1</option>
                                                            <option value="Test2">Test2</option>
                                                            <option value="Test3">Test3</option>
                                                            <option value="Other">Other</option>
                                                        </select>
                                                    </div>
                                                    <button type="submit" class="btn btn-danger">Submit</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `
                        ];

                        dataTable.row.add(rowData);
                    });

                    dataTable.draw();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText);
                    // alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    }

    yearSelector.change(fetchData);
    quarterSelector.change(fetchData);
})

 // This JS is resposible for loading the Approved Payment Sheet Records based on the options selected in Dropdown
var approvedDataTable  = $('.approvedDatatable').DataTable();
const acceptedyearSelector = $('#acceptedPaymentYearSelector');
const acceptedquarterSelector = $('#acceptedQuarterSelector');
    function fetchAcceptedData() {
       
        // alert("Accepted Data");
        var selectedYear = acceptedyearSelector.val();
        var selectedQuarter = acceptedquarterSelector.val();

        if (selectedYear && selectedQuarter) {
          
            $.ajax({
                url: '/get_payment_sheet_data',
                type: 'GET',
                data: { year: selectedYear, quarter: selectedQuarter },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (response) {
                    // alert("Accept Year:" + selectedYear);
                    // alert("Accept Quarter:" + selectedQuarter);
                    approvedDataTable.clear().draw();

                    $.each(response.approved_payment_data, function (index, record) { // Change to approved_payment_data to match your flask endpoint.
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        function formatDate(dateString) {
                              const date = new Date(dateString);
                              const options = {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                              };
                              return date.toLocaleDateString('en-US', options).replace(/,/g, '');
                        }
                        const dateString = record.date; // Simply assign the value
                        const formattedDate = formatDate(dateString);

                        var jrf_srf = '';
                        switch (record.jrf_srf) {
                            case 'jrf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'jrf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'srf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_3':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            default:
                                jrf_srf = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var AdminLabel = '';
                        if (record.admin_action === null || record.admin_action === undefined) {
                            AdminLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.admin_action) {
                                case 'Approved by Admin':
                                    AdminLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                    break;
                                case 'Rejected by Admin':
                                    AdminLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                    break;
                                case 'On Hold by Admin':
                                    AdminLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                    break;
                                default:
                                    AdminLabel = '<span>N/A</span>';
                            }
                        }

                        var AdminButton = '';
                        switch (record.admin_approval) {
                            case 'accepted':
                                AdminButton = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                break;
                            case 'rejected':
                                AdminButton = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                break;
                            case 'hold':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                break;
                            case 'N/A':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                AdminButton = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var HODLabel = '';
                        if (record.hod_action === null || record.hod_action === undefined) {
                            HODLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.hod_action) {
                                case 'Approved by Head of Department':
                                    HODLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Head of Department</span>';
                                    break;
                                case 'Rejected by Head of Department':
                                    HODLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Head of Department</span>';
                                    break;
                                case 'On Hold by Head of Department':
                                    HODLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Head of Department</span>';
                                    break;
                                default:
                                    HODLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var AOLabel = '';
                        if (record.ao_action === null || record.ao_action === undefined) {
                            AOLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.ao_action) {
                                case 'Approved by Account Officer':
                                    AOLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Account Officer</span>';
                                    break;
                                case 'Rejected by Account Officer':
                                    AOLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Account Officer</span>';
                                    break;
                                case 'On Hold by Account Officer':
                                    AOLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Account Officer</span>';
                                    break;
                                default:
                                    AOLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var RegistrarLabel = '';
                        if (record.registrar_action === null || record.registrar_action === undefined) {
                            RegistrarLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.registrar_action) {
                                case 'Approved by Registrar':
                                    RegistrarLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Registrar</span>';
                                    break;
                                case 'Rejected by Registrar':
                                    RegistrarLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Registrar</span>';
                                    break;
                                case 'On Hold by Registrar':
                                    RegistrarLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Registrar</span>';
                                    break;
                                default:
                                    RegistrarLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }
                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)


                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.email,
                            '<strong>' + jrf_srf + '</strong>',
                            record.faculty,
                            formattedDate,
                            'BANRF - ' + record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            '<strong>' + record.total_months + '</strong>' + ' ' + 'Months',
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<strong>INR</strong>' + ' ' + record.total_fellowship,
                            record.hra_rate + ' ' + '<strong>%</strong>',
                            record.hra_amount,
                            record.hra_months,
                            '<strong>INR</strong>' + ' ' + record.total_hra_rate,
                            '<strong>INR</strong>' + ' ' + record.contingency,
                            '<strong>INR</strong>' + ' ' + record.pwd,
                            '<strong>INR</strong>' + ' ' + record.total,
                            '<span class="badge badge-primary bg-primary text-capitalize">' + record.city + '<span>',
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            AdminLabel,
                            HODLabel,
                            AOLabel,
                            RegistrarLabel,
                            `
                               
                                <div class="modal fade" id="acceptModal${record.number}" tabindex="-1" aria-labelledby="acceptModalLabel" style="display: none;">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="acceptModalLabel${record.number}">Accept Applicant</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_accept_payment_sheet" id="acceptForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="accept" value="accept">
                                                    <p style="word-wrap: break-word;">
                                                        Please make sure you want to <span class="text-success fw-bold">Accept</span> the following Payment Sheet :
                                                        <br> <strong>Name:</strong> ${record.full_name}.
                                                        <br> <strong>Fellowship:</strong> ${record.jrf_srf}
                                                        <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                        <br><br>
                                                        After you accept the Payment Sheet,
                                                        <br> it will be passed on to HoD for further approval.
                                                    </p>
                                                    <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="modal fade" id="rejectModal${record.number}" tabindex="-1" aria-labelledby="rejectModalLabel">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="rejectModalLabel${record.number}">Reject Applicant</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_reject_payment_sheet" id="rejectForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="email" value="${record.email}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="reject" value="reject">

                                                        <p style="word-wrap: break-word;">
                                                            Please make sure you want to <span class="text-danger fw-bold">Reject</span> the following Payment Sheet :
                                                            <br> <strong>Name:</strong> ${record.full_name}.
                                                            <br> <strong>Fellowship:</strong> jrf_srf
                                                            <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                            <br><br>
                                                        </p>

                                                    <div class="mb-3">
                                                    <label for="rejectionReason" class="form-label">Rejection Reason</label>
                                                        <select name="rejectionReason" id="rejectionReason" class="form-select">
                                                            <option value="" selected>-- Select a Reason --</option>
                                                            <option value="Missing required documents">Missing required documents</option>
                                                            <option value="Progress Report not uploaded">Progress Report not uploaded</option>
                                                            <option value="Half Yearly Report not uploaded">Half Yearly Report not uploaded</option>
                                                            <option value="House Rent Allowance Report not uploaded">House Rent Allowance Report not uploaded</option>
                                                            <option value="Missing required documents">Missing required documents</option>
                                                            <option value="Expired documents">Expired documents</option>
                                                            <option value="The candidate is double beneficiary">The candidate is double beneficiary</option>
                                                            <option value="Providing inaccurate or falsified information in the application">Providing inaccurate or falsified information in the application</option>
                                                            <option value="Mismatched name on the bank account">Mismatched name on the bank account</option>
                                                            <option value="Payment was already issued">Payment was already issued</option>
                                                            <option value="Failure to submit required financial reports">Failure to submit required financial reports</option>
                                                            <option value="Failure to adhere to the fellowship's code of conduct">Failure to adhere to the fellowships code of conduct</option>
                                                            <option value="Cancellation or suspension of the fellowship program">Cancellation or suspension of the fellowship program</option>
                                                            <option value="Changes in funding priorities">Changes in funding priorities</option>
                                                        </select>
                                                    </div>
                                                    <button type="submit" class="btn btn-danger">Submit Rejection</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div class="modal fade" id="holdModal${record.number}" tabindex="-1" aria-labelledby="holdModalLabel">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="holdModalLabel${record.number}">Hold Payment Sheet</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_hold_payment_sheet" id="holdForm${record.number}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="fellowship_awarded_year" value="${record.fellowship_awarded_year}">
                                                    <input type="hidden" name="hold" value="hold">

                                                        <p style="word-wrap: break-word;">
                                                            Please make sure you want to keep the Payment Sheet <span class="text-warning fw-bold">On Hold</span>:
                                                            <br> <strong>Name:</strong> ${record.full_name}.
                                                            <br> <strong>Fellowship:</strong> ${record.jrf_srf}
                                                            <br> <strong>Total Fellowship Amount:</strong> ${record.fellowship}
                                                            <br><br>
                                                        </p>

                                                    <div class="mb-3">
                                                    <label for="rejectionReason" class="form-label">On Hold Reason</label>
                                                        <select name="onHoldReason" id="onHoldReason" class="form-select">
                                                            <option value="" selected>-- Select a Reason --</option>
                                                            <option value="The candidate is double beneficiary">The candidate is double beneficiary</option>
                                                            <option value="Test1">Test1</option>
                                                            <option value="Test2">Test2</option>
                                                            <option value="Test3">Test3</option>
                                                            <option value="Other">Other</option>
                                                        </select>
                                                    </div>
                                                    <button type="submit" class="btn btn-danger">Submit</button>
                                                </form>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `
                        ];

                        approvedDataTable.row.add(rowData);
                    });

                    approvedDataTable.draw();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText);
                    // alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    }

    acceptedyearSelector.change(fetchAcceptedData);
    acceptedquarterSelector.change(fetchAcceptedData);



// This JS is resposible for loading the Rejected Payment Sheet Records based on the options selected in Dropdown
var rejectedDataTable  = $('.rejectedDatatable').DataTable();
const rejectedyearSelector = $('#rejectedPaymentYearSelector');
const rejectedquarterSelector = $('#rejectedQuarterSelector');
    function fetchRejectedData() {
        // alert("Rejected Data");
        var selectedYear = rejectedyearSelector.val();
        var selectedQuarter = rejectedquarterSelector.val();

        if (selectedYear && selectedQuarter) {
          
            $.ajax({
                url: '/get_payment_sheet_data',
                type: 'GET',
                data: { year: selectedYear, quarter: selectedQuarter },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (response) {
                    // alert("Rejected Year" + selectedYear);
                    // alert("Rejected Quarter" + selectedQuarter);
                    rejectedDataTable.clear().draw();

                    $.each(response.rejected_payment_data, function (index, record) { // Change to rejected_payment_data to match your flask endpoint.
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        function formatDate(dateString) {
                              const date = new Date(dateString);
                              const options = {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                              };
                              return date.toLocaleDateString('en-US', options).replace(/,/g, '');
                        }
                        const dateString = record.date; // Simply assign the value
                        const formattedDate = formatDate(dateString);

                        var jrf_srf = '';
                        switch (record.jrf_srf) {
                            case 'jrf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'jrf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'srf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_3':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            default:
                                jrf_srf = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var AdminLabel = '';
                        if (record.admin_action === null || record.admin_action === undefined) {
                            AdminLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.admin_action) {
                                case 'Approved by Admin':
                                    AdminLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                    break;
                                case 'Rejected by Admin':
                                    AdminLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                    break;
                                case 'On Hold by Admin':
                                    AdminLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                    break;
                                default:
                                    AdminLabel = '<span>N/A</span>';
                            }
                        }

                        var AdminButton = '';
                        switch (record.admin_approval) {
                            case 'accepted':
                                AdminButton = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                break;
                            case 'rejected':
                                AdminButton = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                break;
                            case 'hold':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                break;
                            case 'N/A':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                AdminButton = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var HODLabel = '';
                        if (record.hod_action === null || record.hod_action === undefined) {
                            HODLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.hod_action) {
                                case 'Approved by Head of Department':
                                    HODLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Head of Department</span>';
                                    break;
                                case 'Rejected by Head of Department':
                                    HODLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Head of Department</span>';
                                    break;
                                case 'On Hold by Head of Department':
                                    HODLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Head of Department</span>';
                                    break;
                                default:
                                    HODLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var AOLabel = '';
                        if (record.ao_action === null || record.ao_action === undefined) {
                            AOLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.ao_action) {
                                case 'Approved by Account Officer':
                                    AOLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Account Officer</span>';
                                    break;
                                case 'Rejected by Account Officer':
                                    AOLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Account Officer</span>';
                                    break;
                                case 'On Hold by Account Officer':
                                    AOLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Account Officer</span>';
                                    break;
                                default:
                                    AOLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var RegistrarLabel = '';
                        if (record.registrar_action === null || record.registrar_action === undefined) {
                            RegistrarLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.registrar_action) {
                                case 'Approved by Registrar':
                                    RegistrarLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Registrar</span>';
                                    break;
                                case 'Rejected by Registrar':
                                    RegistrarLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Registrar</span>';
                                    break;
                                case 'On Hold by Registrar':
                                    RegistrarLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Registrar</span>';
                                    break;
                                default:
                                    RegistrarLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }
                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)


                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.email,
                            '<strong>' + jrf_srf + '</strong>',
                            record.faculty,
                            formattedDate,
                            'BANRF - ' + record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            '<strong>' + record.total_months + '</strong>' + ' ' + 'Months',
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<strong>INR</strong>' + ' ' + record.total_fellowship,
                            record.hra_rate + ' ' + '<strong>%</strong>',
                            record.hra_amount,
                            record.hra_months,
                            '<strong>INR</strong>' + ' ' + record.total_hra_rate,
                            '<strong>INR</strong>' + ' ' + record.contingency,
                            '<strong>INR</strong>' + ' ' + record.pwd,
                            '<strong>INR</strong>' + ' ' + record.total,
                            '<span class="badge badge-primary bg-primary text-capitalize">' + record.city + '<span>',
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            AdminLabel,
                            HODLabel,
                            AOLabel,
                            RegistrarLabel,

                        ];

                        rejectedDataTable.row.add(rowData);
                    });

                    rejectedDataTable.draw();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText);
                    // alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    }

    rejectedyearSelector.change(fetchRejectedData);
    rejectedquarterSelector.change(fetchRejectedData);


    // This JS is resposible for loading the Payment Sheet Records that are ON HOLD based on the options selected in Dropdown
var onHoldDataTable  = $('.onHoldDataTable').DataTable();
const onHoldyearSelector = $('#onHoldPaymentYearSelector');
const onHoldquarterSelector = $('#onHoldQuarterSelector');
    function fetchOnHoldData() {
        // alert("ON HOLD Data");
        var selectedYear = onHoldyearSelector.val();
        var selectedQuarter = onHoldquarterSelector.val();

        if (selectedYear && selectedQuarter) {
          
            $.ajax({
                url: '/get_payment_sheet_data',
                type: 'GET',
                data: { year: selectedYear, quarter: selectedQuarter },
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                success: function (response) {
                    // alert("On HOLD Year" + selectedYear);
                    // alert("On HOLD Quarter" + selectedQuarter);
                    onHoldDataTable.clear().draw();

                    $.each(response.on_hold_payment_data, function (index, record) { // Change to on_hold_payment_data to match your flask endpoint.
                        var statusLabel = '';
                        var scrutinyStatusLabel = '';
                        var finalApprovalLabel = '';

                        function formatDate(dateString) {
                              const date = new Date(dateString);
                              const options = {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                              };
                              return date.toLocaleDateString('en-US', options).replace(/,/g, '');
                        }
                        const dateString = record.date; // Simply assign the value
                        const formattedDate = formatDate(dateString);

                        var jrf_srf = '';
                        switch (record.jrf_srf) {
                            case 'jrf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'jrf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">JRF</span>';
                                break;
                            case 'srf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_2':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            case 'srf_3':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark fw-bold text-capitalize">SRF</span>';
                                break;
                            default:
                                jrf_srf = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var AdminLabel = '';
                        if (record.admin_action === null || record.admin_action === undefined) {
                            AdminLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.admin_action) {
                                case 'Approved by Admin':
                                    AdminLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                    break;
                                case 'Rejected by Admin':
                                    AdminLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                    break;
                                case 'On Hold by Admin':
                                    AdminLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                    break;
                                default:
                                    AdminLabel = '<span>N/A</span>';
                            }
                        }

                        var AdminButton = '';
                        switch (record.admin_approval) {
                            case 'accepted':
                                AdminButton = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                break;
                            case 'rejected':
                                AdminButton = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                break;
                            case 'hold':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                break;
                            case 'N/A':
                                AdminButton = '<span class="badge badge-warning bg-warning text-dark text-capitalize">Pending</span>';
                                break;
                            default:
                                AdminButton = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var HODLabel = '';
                        if (record.hod_action === null || record.hod_action === undefined) {
                            HODLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.hod_action) {
                                case 'Approved by Head of Department':
                                    HODLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Head of Department</span>';
                                    break;
                                case 'Rejected by Head of Department':
                                    HODLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Head of Department</span>';
                                    break;
                                case 'On Hold by Head of Department':
                                    HODLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Head of Department</span>';
                                    break;
                                default:
                                    HODLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var AOLabel = '';
                        if (record.ao_action === null || record.ao_action === undefined) {
                            AOLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.ao_action) {
                                case 'Approved by Account Officer':
                                    AOLabel = '<span class="badge badge-success bg-success text-dark fw-bold text-capitalize">Accepted by Account Officer</span>';
                                    break;
                                case 'Rejected by Account Officer':
                                    AOLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Account Officer</span>';
                                    break;
                                case 'On Hold by Account Officer':
                                    AOLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Account Officer</span>';
                                    break;
                                default:
                                    AOLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }


                        var RegistrarLabel = '';
                        if (record.registrar_action === null || record.registrar_action === undefined) {
                            RegistrarLabel = '<span class="text-primary fw-bold text-capitalize">Pending</span>';
                        } else {
                            switch (record.registrar_action) {
                                case 'Approved by Registrar':
                                    RegistrarLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Registrar</span>';
                                    break;
                                case 'Rejected by Registrar':
                                    RegistrarLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Registrar</span>';
                                    break;
                                case 'On Hold by Registrar':
                                    RegistrarLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Registrar</span>';
                                    break;
                                default:
                                    RegistrarLabel = '<span>N/A</span>'; // Use a span for consistency
                            }
                        }
                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)


                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.email,
                            '<strong>' + jrf_srf + '</strong>',
                            record.faculty,
                            formattedDate,
                            'BANRF - ' + record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            '<strong>' + record.total_months + '</strong>' + ' ' + 'Months',
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<strong>INR</strong>' + ' ' + record.total_fellowship,
                            record.hra_rate + ' ' + '<strong>%</strong>',
                            record.hra_amount,
                            record.hra_months,
                            '<strong>INR</strong>' + ' ' + record.total_hra_rate,
                            '<strong>INR</strong>' + ' ' + record.contingency,
                            '<strong>INR</strong>' + ' ' + record.pwd,
                            '<strong>INR</strong>' + ' ' + record.total,
                            '<span class="badge badge-primary bg-primary text-capitalize">' + record.city + '<span>',
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            AdminLabel,
                            HODLabel,
                            AOLabel,
                            RegistrarLabel,
                        ];

                        onHoldDataTable.row.add(rowData);
                    });

                    onHoldDataTable.draw();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX Error:", status, error, xhr.responseText);
                    // alert('Failed to fetch data. Please check the console for details.');
                }
            });
        }
    }

    onHoldyearSelector.change(fetchOnHoldData);
    onHoldquarterSelector.change(fetchOnHoldData);



// ------------------BEGIN Functions to Update the Page titles Dynamically --------------------------------------------------
// --------------------------------------------------------------------------------
// JS to update the table headings for Main Payment Sheet Report-------------------

function updateTitle() {
  const selectedYear = $('#paymentYearSelector').val()
  const selectedQuarter = $('#quarterSelector').val()

//   console.log("Main Year:",selectedYear )
//   console.log("Main Quarter:",selectedQuarter )

    if (selectedYear && selectedQuarter) {
      const yearNumber = parseInt(selectedYear); // Convert to number
      if (!isNaN(yearNumber)) { //check if yearNumber is a number.
        val = 'BANRF ' + selectedYear ;
      } else {
        val = "Invalid year";
      }
    $('#paymentSheetTitle').html(`Payment Sheet of <span style="font-weight: bold; color: blue;">${selectedQuarter}</span> for <span style="font-weight: bold; color: red;">${val}</span>`)

    } else {
        val = "Please select Year and Quarter";
        $('#paymentSheetTitle').html(`<span style="font-weight: bold; color: red;">${val}</span>`)
    }
}

$(document).on('change','#paymentYearSelector', function(){
    updateTitle()
})
$(document).on('change','#quarterSelector', function(){
    updateTitle()
})
// updateTitle()

// --------------------------------------------------------------------------------


// --------------------------------------------------------------------------------
// JS to update the table headings for Accepted Payment Sheet Report---------------
function updateAcceptedTitle() {

    const selectedYear = $('#acceptedPaymentYearSelector').val()
    const selectedQuarter = $('#acceptedQuarterSelector').val()

    // const selectedYear = acceptedyearDropdown.value;
    // const selectedQuarter = acceptedQuarter.value;
        if (selectedYear && selectedQuarter) {
        const yearNumber = parseInt(selectedYear); // Convert to number
            if (!isNaN(yearNumber)) { //check if yearNumber is a number.
                val = 'BANRF ' + selectedYear ;
            } else {
                val = "Invalid year";
            }
            $('#acceptedpaymentSheetTitle').html(`Payment Sheet of <span style="font-weight: bold; color: blue;">${selectedQuarter}</span> for <span style="font-weight: bold; color: red;">${val}</span>`)

        } else {
            val = "Please select Year and Quarter";
            $('#acceptedpaymentSheetTitle').html(`<span style="font-weight: bold; color: red;">${val}</span>`)
        }
}
$(document).on('change','#acceptedPaymentYearSelector', function(){
    updateAcceptedTitle()
})
$(document).on('change','#acceptedQuarterSelector', function(){
    updateAcceptedTitle()
})
// updateAcceptedTitle()

//Initial call to update title.

// --------------------------------------------------------------------------------

// --------------------------------------------------------------------------------
//  JS to update the table headings for Rejected Payment Sheet Report--------------
// Function to update the titles for Rejected Payment Sheet
function updateRejectedTitle() {

  const selectedYear = $('#rejectedPaymentYearSelector').val()
  const selectedQuarter = $('#rejectedQuarterSelector').val()
    if (selectedYear && selectedQuarter) {
      const yearNumber = parseInt(selectedYear); // Convert to number
      if (!isNaN(yearNumber)) { //check if yearNumber is a number.
        val = 'BANRF ' + selectedYear ;
      } else {
        val = "Invalid year";
      }
        $('#rejectedpaymentSheetTitle').html(`Payment Sheet of <span style="font-weight: bold; color: blue;">${selectedQuarter}</span> for <span style="font-weight: bold; color: red;">${val}</span>`)

    } else {
        val = "Please select Year and Quarter";
        $('#rejectedpaymentSheetTitle').html(`<span style="font-weight: bold; color: red;">${val}</span>`)
    }
    
}
$(document).on('change','#rejectedPaymentYearSelector', function(){
    updateRejectedTitle()
})
$(document).on('change','#rejectedQuarterSelector', function(){
    updateRejectedTitle()
})

//Initial call to update title.
// updateRejectedTitle();
// -----------------------------------------------------------------------------------------

// -----------------------------------------------------------------------------------------
//  JS to update Title of On HOLD Payment Sheet Reports ------------------------------------
// Function to update the titles for Approved Payment Sheet
function updateOnHoldTitle() {

  const selectedYear = $('#onHoldPaymentYearSelector').val()
  const selectedQuarter = $('#onHoldQuarterSelector').val()
    if (selectedYear && selectedQuarter) {
      const yearNumber = parseInt(selectedYear); // Convert to number
      if (!isNaN(yearNumber)) { //check if yearNumber is a number.
        val = 'BANRF ' + selectedYear ;
      } else {
        val = "Invalid year";
      }
       $('#onHoldpaymentSheetTitle').html(`Payment Sheet of <span style="font-weight: bold; color: blue;">${selectedQuarter}</span> for <span style="font-weight: bold; color: red;">${val}</span>`);

    } else {
        val = "Please select Year and Quarter";
        $('#onHoldpaymentSheetTitle').html(`<span style="font-weight: bold; color: red;">${val}</span>`)
    }
}

$(document).on('change','#onHoldPaymentYearSelector', function(){
    updateOnHoldTitle()
})
$(document).on('change','#onHoldQuarterSelector', function(){
    updateOnHoldTitle()
})


//Initial call to update title.
updateTitle();
updateAcceptedTitle();
updateRejectedTitle();
updateOnHoldTitle();
//Initial call to update title.
// --------------------------------------------------------------------------------
// ------------------END Functions to Update the Page titles Dynamically --------------------------------------------------

