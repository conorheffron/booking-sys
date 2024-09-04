function dateChangeHandler(e) {
    e.preventDefault();

    date = document.querySelectorAll('input#id_reservation_date').value;
    let formdata = new FormData(this);
    let booking_date = formdata.get("reservation_date");

    if (isValidDate(booking_date)) {
        renderTable(booking_date);
    }
}

function submitHandler(e) {
    e.preventDefault();

    fetch(form.action, { method: 'POST', body: new FormData(form) })
        .then(response => response.json())
        .then(response => {
            alert(response.message);
            bookings_by_date = response.reservations
            console.log(bookings_by_date)
            form.reset();
            renderTableBookings(bookings_by_date)
        });
}

function renderTable(booking_date) {
    console.log(booking_date)
    try {
        fetch('/bookings?date=' + booking_date)
            .then(response => response.json())
            .then(response => {
                console.log(response);
                bookings_by_date = response.reservations
                renderTableBookings(bookings_by_date)
            });
    } catch (e) {
        console.log(e);
    }
}

function renderTableBookings(bookings) {
    var k = '<tbody>'
    k += '<tr>';
    k += '<th>First Name</td>';
    k += '<th>Reservation Date</td>';
    k += '<th>Reservation Time</td>';
    k += '</tr>';
    for (i = 0; i < bookings.length; i++) {
        k += '<tr>';
        k += '<td>' + bookings[i]["first_name"] + '</td>';
        k += '<td>' + bookings[i]["reservation_date"] + '</td>';
        k += '<td>' + bookings[i]["reservation_slot"] + '</td>';
        k += '</tr>';
    }
    k += '</tbody>';
    document.getElementById('tableData').innerHTML = k;
}

function refresh(){
    window.location.reload()
}

function getCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    return yyyy + '-' + mm + '-' + dd;
}

function isValidDate(date) {
    d = new Date(date);
    return d instanceof Date && !isNaN(d);
}