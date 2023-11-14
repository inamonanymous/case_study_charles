document.addEventListener('DOMContentLoaded', function() {
    fetchDataAndDisplay();
});

function fetchDataAndDisplay() {
    axios.get('/dashboard-items')  // Replace with your actual API endpoint
        .then(function (response) {
            const data = response.data;
            updateCount('productsCount', data.products_count);
            updateCount('salesCount', data.sales_count);
            updateCount('tradesCount', data.trades_count);
            updateCount('locationCount', data.location_count);
            updateCount('guestCount', data.guest_count);
            updateCount('pendingCount', data.pending_account_count);
            updateCount('adminCount', data.admin_count);
            // Add similar calls for trades and location
        })
        .catch(function (error) {
            console.error('Error fetching data:', error);
        });
}

function updateCount(elementId, count) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = count;
    }
}