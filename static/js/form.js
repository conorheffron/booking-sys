window.onload = function () {
    // set listeners for form submit & for 'onChange' reservation date input
    const form = document.getElementById('form');
    form.addEventListener("submit", submitHandler);
    form.addEventListener("input", dateChangeHandler)

    // render bookings by current date by default
    renderTable(getCurrentDate())
};