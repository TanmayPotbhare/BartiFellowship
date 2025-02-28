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


                        var jrf_srf = '';
                        switch (record.jrf_srf) {
                            case 'jrf_1':
                                jrf_srf = '<span class="badge badge-success bg-success text-capitalize">JRF</span>';
                                break;
                            case 'jrf_2':
                                jrf_srf = '<span class="badge badge-danger bg-danger text-capitalize">JRF</span>';
                                break;
                            case 'srf_1':
                                jrf_srf = '<span class="badge badge-warning bg-warning text-dark text-capitalize">SRF</span>';
                                break;
                            case 'srf_2':
                                jrf_srf = '<span class="badge badge-primary text-dark text-capitalize">SRF</span>';
                                break;
                            case 'srf_3':
                                jrf_srf = '<span class="badge badge-primary text-dark text-capitalize">SRF</span>';
                                break;
                            default:
                                jrf_srf = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var AdminLabel = '';
                        switch (record.admin_action) {
                            case 'Accepted by Admin':
                                AdminLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Admin</span>';
                                break;
                            case 'Rejected by Admin':
                                AdminLabel = '<span class="badge badge-danger bg-danger text-capitalize">Rejected by Admin</span>';
                                break;
                            case 'On Hold by Admin':
                                AdminLabel = '<span class="badge badge-warning bg-warning text-dark text-capitalize">On Hold by Admin</span>';
                                break;
                            default:
                                AdminLabel = '<span>N/A</span>'; // Use a span for consistency
                        }

                        var HODLabel = '';
                        switch (record.hod_action) {
                            case 'Accepted by Head of Department':
                                HODLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Head of Department</span>';
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

                        var AOLabel = '';
                        switch (record.ao_action) {
                            case 'Accepted by Account Officer':
                                AOLabel = '<span class="badge badge-success bg-success text-capitalize">Accepted by Account Officer</span>';
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

                        var RegistrarLabel = '';
                        switch (record.registrar_action) {
                            case 'Accepted by Registrar':
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

                        // ... (statusLabel, scrutinyStatusLabel, finalApprovalLabel logic remains the same)


                        var rowData = [
                            index + 1,
                            record.applicant_id,
                            record.full_name,
                            record.email,
                            '<strong>' + jrf_srf + '</strong>',
                            record.faculty,
                            record.date,
                            record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            record.total_months,
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            '<strong>INR</strong>' + ' ' + record.total_fellowship,
                            record.hra_rate + ' ' + '<strong>%</strong>',
                            record.hra_amount,
                            record.hra_months,
                            '<strong>INR</strong>' + ' ' + record.total_hra_rate,
                            '<strong>INR</strong>' + ' ' + record.contingency,
                            '<strong>INR</strong>' + ' ' + record.pwd,
                            '<strong>INR</strong>' + ' ' + record.total,
                            '<strong class="text-danger">' + record.city + '<strong>',
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
        val = 'BANRF ' + selectedYear ;
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