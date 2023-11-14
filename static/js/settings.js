function updateUserInfo(id) {
    // Get updated user information
    var firstname = document.getElementById("firstname").value;
    var surname = document.getElementById("surname").value;
    var phone = document.getElementById("phone").value;
    var email = document.getElementById("email").value;

    // Send updated information to the server
    var formData = {
        'firstname': firstname,
        'surname': surname,
        'phone': phone,
        'email': email,
    };

    axios.put(`/update-user-info/${id}`, formData)
        .then(function (response) {
            console.log(response.data);
            alert('User information updated successfully!');
            location.reload(true);
        })
        .catch(function (error) {
            console.error('Error updating user information:', error);
            alert(`Error updating user information ${error}`);
        });
}