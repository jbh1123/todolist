document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/login'); // The formaction attribute value

    // Define what happens on successful data submission
    xhr.onload = function() {
        if (xhr.status === 200) {
            // Redirect to index.html
            window.location.href = 'index';
        } else if (xhr.status === 401 ) {
            // Invalid login
            alert('Invalid credentials. Please try again.');
        } else {
            alert('Request failed. Returned status of ' + xhr.status);
        }
    };

    // Set up our request
    var formData = new FormData(this);

    // Finally, send the data.
    xhr.send(formData);
});

let addNewUserButton = document.getElementById("addUser");

let addNewUser = function () {
    window.location.href = '/adduser';
}

addNewUserButton.addEventListener("click", addNewUser);