document.addEventListener('DOMContentLoaded', function () {
    // Fetch locations from the server and populate the dropdown
        axios.get('/get-products-and-locations')
            .then(function (response) {
                response.data.locations_data.forEach(function (a) {
                    var option = document.createElement('option');
                    option.value = a.location_id;
                    option.text = a.location_name;
                    document.getElementById('location').appendChild(option);
                });
            })
            .catch(function (error) {
                console.error('Error fetching locations:', error);
        });       
    });
    function signUpEntry(){
            firstname = document.getElementById("firstname").value;
            surname = document.getElementById("surname").value;
            phone = document.getElementById("phone").value;
            username = document.getElementById("username").value;
            password = document.getElementById("password").value;
            email = document.getElementById("email").value;
            locationID = document.getElementById("location").value;

            formData = {
                'firstname': firstname,
                'surname': surname,
                'phone': phone,
                'username': username,
                'password': password,
                'email': email,
                'location_id': locationID,
            }

            axios.post('/sign-up-entry', formData)
                    .then(function (response) {
                        console.log(response.data)
                        alert('Sign up successful!');
                        window.location.href="../";
                    })
                    .catch(function (error) {
                        console.error('Error submitting form:', error);
                        console.log(formData)
                });
        }