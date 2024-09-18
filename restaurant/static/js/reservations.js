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
            // form.reset();
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
    if (bookings.length > 0) {
        var dynamoT = '<tbody>'
        dynamoT += '<tr>';
        dynamoT += '<th>Name</td>';
        dynamoT += '<th>Booking Date</td>';
        dynamoT += '<th>Booking Time</td>';
        dynamoT += '</tr>';
        for (i = 0; i < bookings.length; i++) {
            dynamoT += '<tr>';
            dynamoT += '<td>' + bookings[i]["first_name"] + '</td>';
            dynamoT += '<td>' + bookings[i]["reservation_date"] + '</td>';
            dynamoT += '<td>' + bookings[i]["reservation_slot"] + '</td>';
            dynamoT += '</tr>';
        }
        dynamoT += '</tbody>';
        document.getElementById('tableData').innerHTML = dynamoT;
    } else {
        document.getElementById('tableData').innerHTML = '<tbody id="tableData"></tbody>';
    }
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