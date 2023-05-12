"use strict";
function submitRecoverAccountForm(event) {
    event.preventDefault();
    const recoverAccountData = getRecoverAccountFormData();
    sendRecoverAccountRequest(recoverAccountData)
        .then((response) => response.json())
        .then(checkStatus)
        .catch((error) => {
        console.log(error);
    });
}
function getRecoverAccountFormData() {
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const confirm_password = document.querySelector('input[name="confirm_password"]').value;
    return {
        email,
        password,
        confirm_password,
    };
}
function sendRecoverAccountRequest(data) {
    const formData = new URLSearchParams(data).toString();
    return fetch("/recover", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
    });
}
function addRecoverAccountEventListener() {
    const recover_account_form = document.getElementById("recover_account");
    if (recover_account_form === null)
        return;
    recover_account_form.addEventListener("submit", submitRecoverAccountForm);
}
window.addEventListener("load", addRecoverAccountEventListener);
//# sourceMappingURL=recover_account.js.map