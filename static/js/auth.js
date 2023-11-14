function login(){
    var loginUsername = document.getElementById("login_username").value;
    var loginPassword = document.getElementById("login_password").value;

    var formData = {
        'username': loginUsername,
        'password': loginPassword
    }

    axios.post('/auth', formData).then(response => {
        window.location.href = "/home";
        console.log(response.data);
    }).catch(error => {
        location.reload(true);
    });
}