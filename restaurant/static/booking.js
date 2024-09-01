window.onload = function() {
    renderTable(getCurrentDate())

    const form = document.getElementById('form');
    form.addEventListener("submit", submitHandler);
    form.addEventListener("input", dateChangeHandler)

    function dateChangeHandler(e) {
        e.preventDefault();

        date = document.querySelectorAll('input#id_reservation_date').value;
        let formdata = new FormData(this);
        let booking_date = formdata.get("reservation_date");
        console.log(booking_date);

        if (isValidDate(booking_date)) {
            renderTable(booking_date);
        }
    }

    function submitHandler(e) {
        e.preventDefault();

        fetch(form.action, {method:'POST', body: new FormData(form)})
        .then(response=>response.json())
        .then(data=>{
                alert(data.message);
                console.log(data.reservations)
                form.reset();
        });
    }
  };

function renderTable(booking_date) {
    try {
        fetch(`/bookings/${booking_date}`)
            .then(response => response.json())
            .then(response => {
            console.log(response);
            bookings_by_date = response.reservations
            if (bookings_by_date.length > 0) {
                var k = '<tbody>'
                k+= '<tr>';
                k+= '<th>First Name</td>';
                k+= '<th>Reservation Date</td>';
                k+= '<th>Reservation Time</td>';
                k+= '</tr>';
                for(i = 0;i < bookings_by_date.length; i++){             
                    k+= '<tr>';
                    k+= '<td>' + bookings_by_date[i]["first_name"] + '</td>';
                    k+= '<td>' + bookings_by_date[i]["reservation_date"] + '</td>';
                    k+= '<td>' + bookings_by_date[i]["reservation_slot"] + '</td>';
                    k+= '</tr>';
                }
                k+='</tbody>';
                document.getElementById('tableData').innerHTML = k;
            } else {
                document.getElementById('tableData').innerHTML = '<tbody></tbody>';
            }
            });
        } catch (e) {
        console.log(e);
        }
}

function getCurrentDate() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); 
    var yyyy = today.getFullYear();
    return yyyy + '-' + mm + '-' + dd ;
}

function isValidDate(date) {
    d = new Date(date);
    return d instanceof Date && !isNaN(d);
    }