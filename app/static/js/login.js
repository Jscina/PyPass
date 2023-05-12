"use strict";
function redirectToHomePage() {
    window.location.href = "/home";
}
function displayErrorMessage(message) {
    let error = document.getElementById("error_msg");
    if (error === null)
        return;
    error.innerText = message;
}
function checkStatus(data) {
    console.log(data);
    switch (data.status) {
        case "success":
            redirectToHomePage();
            break;
        default:
            displayErrorMessage(data.message);
            break;
    }
}
function submitLoginForm(username, password) {
    fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
        checkStatus(data);
    })
        .catch((error) => {
        console.log(error);
    });
}
function handleLoginFormSubmit(event) {
    event.preventDefault();
    const username = document.querySelector('input[name="username"]');
    const password = document.querySelector('input[name="password"]');
    submitLoginForm(username.value, password.value);
}
function addLoginEventListener() {
    const login_form = document.getElementById("login");
    if (login_form === null)
        return;
    login_form.addEventListener("submit", handleLoginFormSubmit);
}
window.addEventListener("load", addLoginEventListener);
//# sourceMappingURL=login.js.map