window.onload = function () {
    renderVersion();
}

function renderVersion() {
    fetch('/version/')
        .then(async response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            let appVers = await response.text();
            document.getElementById('appVersion').innerHTML =  '<a class="nav-link" target="_blank" href="https://github.com/conorheffron/booking-sys">GitHub Version: ' + appVers + '</a>';
        })
        .then(data => console.log(data))
        .catch(error => console.error('Fetch error:', error));
}
