"use strict";
function submitCreateAccountForm(event) {
    event.preventDefault();
    const createAccountData = getCreateAccountFormData();
    sendCreateAccountRequest(createAccountData)
        .then((response) => {
        if (response.redirected)
            redirectToHomePage();
        else
            return response.json();
    })
        .then(handleCreateAccountResponse)
        .catch((error) => {
        console.log(error);
    });
}
function getCreateAccountFormData() {
    const username = document.querySelector('input[name="username"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const confirm_password = document.querySelector('input[name="confirm_password"]').value;
    return {
        username,
        email,
        password,
        confirm_password,
    };
}
function sendCreateAccountRequest(data) {
    return fetch("/create_account", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
}
function handleCreateAccountResponse(data) {
    if (data === undefined)
        return;
    if (data.status === "error") {
        const error_msg = document.getElementById("error_msg");
        error_msg.innerText = data.message;
    }
}
function addCreateAccountEventListenter() {
    const create_account_form = document.getElementById("create_account");
    if (create_account_form === null)
        return;
    create_account_form.addEventListener("submit", submitCreateAccountForm);
}
window.addEventListener("load", addCreateAccountEventListenter);
//# sourceMappingURL=create_account.js.map