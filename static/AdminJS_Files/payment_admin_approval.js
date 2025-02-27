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
                            record.number,
                            record.full_name,
                            record.date,
                            record.fellowship_awarded_year,
                            record.duration_date_from + ' ' + '<strong> TO </strong>' + ' ' + record.duration_date_to,
                            record.bank_name,
                            record.account_number,
                            record.ifsc_code,
                            '<strong>INR</strong>' + ' ' + record.fellowship,
                            `
                                <td>
                                    <form method="POST">
                                    <input type="hidden" name="sheet_id" value="{{ record['number'] }}">
                                        <button class="btn btn-success btn-sm tooltip-trigger" type="button" data-bs-toggle="modal" data-bs-target="#acceptModal"
                                            data-applicant-id="{{ record['number'] }}" data-bs-placement="top"
                                            data-bs-original-title="Accept Sheet">
                                            <i class="mdi mdi-check-all"></i>
                                        </button>
                                        <button class="btn btn-danger btn-sm tooltip-trigger" type="button" data-bs-toggle="modal" data-bs-target="#rejectModal"
                                            data-applicant-id="{{ record['number'] }}" data-bs-placement="top"
                                            data-bs-original-title="Reject Sheet">
                                            <i class="mdi mdi-close-octagon"></i>
                                        </button>
                                        <button class="btn btn-warning btn-sm tooltip-trigger" type="button" data-bs-toggle="modal" data-bs-target="#holdModal"
                                            data-applicant-id="{{ record['number'] }}" data-bs-placement="top"
                                            data-bs-original-title="Hold Sheet">
                                            <i class="mdi mdi-close-octagon"></i>
                                        </button>
                                    </form>
                                </td>

                                <div class="modal fade" id="acceptModal${index + 1}" tabindex="-1" aria-labelledby="acceptModalLabel${index + 1}" style="display: none;">
                                    <div class="modal-dialog">
                                        <div class="modal-content">
                                            <div class="modal-header">
                                                <h5 class="modal-title" id="acceptModalLabel${index + 1}">Accept Applicant</h5>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <form action="/admin_accept" id="acceptForm${index + 1}" method="POST">
                                                    <input type="hidden" name="sheet_id" value="${record.number}">
                                                    <input type="hidden" name="accept" value="accept">
                                                    <p style="word-wrap: break-word;">
                                                        Please make sure you want to <span class="text-success fw-bold">Accept</span> the following Payment Sheet :
                                                        <br> <strong>Name:</strong> {{ record['full_name'] }}.
                                                        <br> <strong>Fellowship:</strong> {{ record['jrf_srf'] }}
                                                        <br> <strong>Total Fellowship Amount:</strong> {{ record['total_fellowship'] }}
                                                        <br><br>
                                                        After you accept the Payment Sheet, it will be passed on to HoD for further approval.
                                                    </p>
                                                    <button type="submit" class="btn btn-success text-dark">Submit Acceptance</button>
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