fetchUserData();
function getLoginTypeText(loginType) {
    if (loginType === 4096) {
        return 'Admin';
    } else if (loginType === 128) {
        return 'Guest';
    } else if (loginType === null) {
        return 'UNVERIFIED';
    } else {
        return loginType;
    }
}

function populateUsersTable(users) {
    const usersTableBody = document.getElementById('users-table').getElementsByTagName('tbody')[0];

    users.forEach(user => {
        let row = usersTableBody.insertRow();
        row.innerHTML = `
            <td>${user.user_id}</td>
            <td>${user.username}</td>
            <td>${user.firstname}</td>
            <td>${user.surname}</td>
            <td>${user.location_id}</td>
            <td>${user.email}</td>
            <td>${getLoginTypeText(user.login_type)}</td>
            <td><button onclick="verifyUser(${user.user_id})">Verify</button></td>
            <td><button onclick="deleteUser(${user.user_id})">Delete</button></td>
        `;
    });
}

function verifyUser(id){
    if (confirm("Are you sure you want to verify this user?")){
        axios.put(`/verify-user-data/${id}`).then(response => {
            alert("User Verified");
            location.reload(true);
        }).catch(error => {
            alert(error.response.data.message);
            console.log(error)
        })
    }
}

function deleteUser(id){
    if (confirm("Are you sure you want to delete this user?")){
        axios.delete(`/delete-user-data/${id}`).then(response => {
            alert("User deleted!");
            location.reload(true);
        }).catch(error => {
            alert(error.response.data.message);
            console.log(error)
        });
    }
}

function fetchUserData(){
    axios.get('/get-users-data').then(response => {
        console.log(response.data)
        populateUsersTable(response.data);
    }).catch(error => {
        console.log(error)
    });
}