/**
 * On load of index.html
 * Check if user has authenticated
 * if true do nothing, else redirect to access denied page
 */
window.addEventListener('load', (event) => {
    const logged_in = window.localStorage.getItem("Login");
    const name = window.localStorage.getItem("Name")

    if (logged_in == "true") {
        document.getElementById("logged-in-user").innerHTML = name;
    }
    else {
        window.location.href = "401.html"
    }

});