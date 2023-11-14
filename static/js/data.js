// Add these functions to your existing JavaScript

function openEditLocationModal(id) {
    document.getElementById('editLocationModal').style.display = 'block';
    document.getElementById('locationReadId').innerText = `Location ID: ${id}`; 
    axios.get(`/manage-locations/${id}`).then(response => {
        document.getElementById('locationId').value = id;
        document.getElementById('locationReadId1').value = id; 
        document.getElementById('newLocationName').value=response.data.location_name;    
    })
}
  
function closeEditLocationModal() {
    document.getElementById('locationId').value = '';
    document.getElementById('editLocationModal').style.display = 'none';
}

function openEditProductModal(id) {
    document.getElementById('editProductModal').style.display = 'block';
    document.getElementById('productReadId').innerText = `Product ID: ${id}`; 
    
    axios.get(`/manage-products/${id}`).then(response => {
        document.getElementById('productId').value = id;
        document.getElementById('productReadId1').value = id; 
        document.getElementById('newProductName').value=response.data.product_name;    
        document.getElementById('newProductDescription').value=response.data.product_description;    
        document.getElementById('newProductUnit').value=response.data.product_unit;    
    })
  }
  
  function closeEditProductModal() {
    document.getElementById('productId').value = '';
    document.getElementById('editProductModal').style.display = 'none';
  }


function hideAllContainers() {
    var formContainers = document.querySelectorAll('.form-container');
    var tableContainers = document.querySelectorAll('.table-container');

    // Hide all form and table containers
    formContainers.forEach(function(container) {
        container.style.display = 'none';
    });
    tableContainers.forEach(function(container) {
        container.style.display = 'none';
    });
}

function showActionSelect() {
    var manageSelection = document.getElementById('manage-selection').value;
    var actionSelectContainer = document.getElementById('action-select-container');

    hideAllContainers();

    // Reset action selection and show/hide action select container
    var actionSelect = document.getElementById('action-selection');
    actionSelect.value = '';
    actionSelectContainer.style.display = manageSelection ? 'block' : 'none';
}

function showForm() {
    var manageSelection = document.getElementById('manage-selection').value;
    var action = document.getElementById('action-selection').value;
    var formContainerId = manageSelection + '-form';
    var tableContainerId = manageSelection + '-table';

    hideAllContainers();

    // Show the selected form or table container based on action
    if (action === 'add') {
        var formContainer = document.getElementById(formContainerId);
        if (formContainer) {
            formContainer.style.display = 'block';
        }
    } else if (action === 'edit') {
        var tableContainer = document.getElementById(tableContainerId);
        if (tableContainer) {
            tableContainer.style.display = 'block';
        }
    }
}

function deleteTrade(id){
    if (confirm("Are you sure you want to delete this Record?")){
        axios.delete(`/manage-trades/${id}`).then(response => {
            alert("Trade record deleted");
            location.reload(true);
        }).catch(error => {
            alert(error);
            console.log(error);
        });
    }
}

function deleteLocation(id){
    if (confirm("Are you sure you want to delete this location?")){
        axios.delete(`/manage-locations/${id}`).then(response => {
            alert("Location deleted with its child rows");
            location.reload(true);
        }).catch(error => {
            alert(error);
            console.log(error)
            
        });
    }
}

function editLocation(){
    var locationId = document.getElementById('locationId').value;
    var locationName = document.getElementById('newLocationName').value;
    
    var formData = {
        'location_name': locationName,
    }
    if (confirm("Are you sure you want to update this location")){
        axios.put(`/manage-locations/${locationId}`, formData).then(response => {
            alert("location updated")
            location.reload(true);
        }).catch(error => {
            alert(error)
        });
     }
}
function deleteProduct(id){
    if (confirm("Are you sure you want to delete this product?")){
        axios.delete(`/manage-products/${id}`).then(response => {
            alert("Product deleted with its child rows");
            location.reload(true);
        }).catch(error => {
            alert(error);
            console.log(error)
        });
    }
}

function editProduct(){
    var productId = document.getElementById('productId').value;
    var productName = document.getElementById('newProductName').value;
    var productDescription = document.getElementById('newProductDescription').value;
    var productUnit = document.getElementById('newProductUnit').value;
    var formData = {
        'product_name': productName,
        'product_description': productDescription,
        'product_unit': productUnit
    }
    if(confirm("Are you sure you want to update this product?")){
        axios.put(`/manage-products/${productId}`, formData).then(response => {
            alert("product updated")
            location.reload(true);
        }).catch(error => {
            alert(error)
        });
    }
}

function addProduct(){
    var productName = document.getElementById('product_name').value ;
    var productDescription = document.getElementById('product_description').value;
    var productUnit = document.getElementById('product_unit').value;

    formData = {
        'product_name': productName,
        'product_description': productDescription,
        'product_unit': productUnit
    }

    axios.post('/add-product', formData).then(respone => {
        alert("Item added to Product");
        location.reload(true);
    }).catch(error => {
        console.log(error);
        alert("Cant add Product")
    })

    
}

function addLocation(){
    var locationName = document.getElementById('location_name').value;
    var formData = {
        'location_name': locationName
    };

    axios.post('/add-location', formData).then(respone => {
        alert("Item added to Location");
        location.reload(true);
    }).catch(error => {
        console.log(error);
        alert("Cant add Location");
    })
}

function addTrade(){
    var locationId = document.getElementById('trade_location').value;
    var tradeProduct = document.getElementById('trade_product').value;
    var tradeYear = document.getElementById('trade_year').value;
    var tradeQuantity = document.getElementById('trade_quantity').value;

    var formData = {
        'location_id': locationId,
        'trade_product': tradeProduct,
        'trade_year': tradeYear,
        'trade_quantity': tradeQuantity
    }

    axios.post('/add-trade', formData).then(response => {
        alert("Item added to Product");
        location.reload(true);
    }).catch(error => {
        console.log(error.data);
        alert("Cant add Trade");
    })
}

document.addEventListener("DOMContentLoaded", function () {
// Fetch locations and products data
axios.get('/get-products-and-locations').then(response => {
    var locationsData = response.data.locations_data;
    var productsData = response.data.products_data;
    
    var locationSelect = document.getElementById('trade_location');
    var productSelect = document.getElementById('trade_product');

    // Clear existing options before adding new ones
    locationSelect.innerHTML = '<option value="" selected disabled>Select Location</option>';
    productSelect.innerHTML = '<option value="" selected disabled>Select Product</option>';

    // Populate locations dropdown
    locationsData.forEach(function (location) {
        var option = document.createElement('option');
        option.value = location.location_id;
        option.text = location.location_name;
        locationSelect.appendChild(option);
    });

    // Populate products dropdown
    productsData.forEach(function (product) {
        var option = document.createElement('option');
        option.value = product.product_id;
        option.text = product.product_name;
        productSelect.appendChild(option);
    });
}).catch(error => {
    console.error('Error fetching data:', error);
});
});

function populateProductsTable(products) {
    const productsTableBody = document.getElementById('products-table').getElementsByTagName('tbody')[0];
    products.forEach(product => {
        let row = productsTableBody.insertRow();
        row.innerHTML = `
            <td>${product.product_id}</td>
            <td>${product.product_name}</td>
            <td>${product.product_description || ''}</td>
            <td>${product.product_unit}</td>
            <td><button onclick="openEditProductModal(${product.product_id})">Edit</button></td>
            <td><button onclick="deleteProduct(${product.product_id})">Delete</button></td>
        `;
    });
}

// Function to populate the Locations table
function populateLocationsTable(locations) {
    const locationsTableBody = document.getElementById('locations-table').getElementsByTagName('tbody')[0];
    locations.forEach(location => {
        let row = locationsTableBody.insertRow();
        row.innerHTML = `
            <td>${location.location_id}</td>
            <td>${location.location_name}</td>
            <td onclick="openEditLocationModal(${location.location_id})"><button>Edit</button></td>
            <td><button onclick="deleteLocation(${location.location_id})">Delete</button></td>
        `;
    });
}

// Function to populate the Trades table
function populateTradesTable(trades) {
    const tradesTableBody = document.getElementById('trade-data-table').getElementsByTagName('tbody')[0];

    trades.forEach((trade, index) => {
        let row = tradesTableBody.insertRow();
        row.innerHTML = `
            <td>${trade.trade_id}</td>
            <td>${trade.location_name}</td>
            <td>${trade.product_name}</td>
            <td>${trade.trade_year}</td>
            <td>${trade.trade_quantity}</td>
            <td><button onclick="deleteTrade(${trade.trade_id})">Delete</button></td>
        `;
    });
}


document.addEventListener("DOMContentLoaded", function () {
    // Fetch data from your API/server
    // Assuming you have functions to fetch data like getProducts(), getLocations(), getTrades()
    axios.get('/get-product-location-trade').then(response => {
        populateProductsTable(response.data.products);
        populateLocationsTable(response.data.locations);
        populateTradesTable(response.data.trades);
    }).catch(error => {

    });

    // Populate tables
});