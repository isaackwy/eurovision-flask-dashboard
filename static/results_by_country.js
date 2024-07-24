document.addEventListener('DOMContentLoaded', function() {

    let country_dropdown = document.getElementById('country_dropdown');

    country_dropdown.addEventListener('change', function() {
        country_dropdown.submit();
    });
});
