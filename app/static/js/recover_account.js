"use strict";
function showError(error) {
    const error_msg = document.querySelector(".error-msg");
    error_msg.classList.remove("hide");
    error_msg.innerHTML = `<p>${error}</p>`;
}
function resetForms() {
    const recoverAccountForm = document.getElementById("recover_account");
    const securityCodeForm = document.getElementById("enter_code");
    const changePasswordForm = document.getElementById("change_password");
    recoverAccountForm.classList.remove("hide");
    securityCodeForm.classList.add("hide");
    changePasswordForm.classList.add("hide");
}
function sendRecoverEmail(email) {
    localStorage.setItem("recover_email", email);
    fetch("/send_recovery_email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ recovery_email: email }),
    })
        .then((response) => {
        if (!response.ok) {
            throw new Error("Response was not ok");
        }
        return response.json();
    })
        .then(() => {
        const recoverAccountForm = document.getElementById("recover_account");
        const securityCodeForm = document.getElementById("enter_code");
        recoverAccountForm.classList.add("hide");
        securityCodeForm.classList.remove("hide");
    })
        .catch((error) => {
        showError(error);
    });
}
function verifyCode(securityCode) {
    fetch("/verify_code", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            confirm_code: securityCode,
        }),
    })
        .then((response) => {
        return response.json();
    })
        .then((data) => {
        if (data.status === "failure")
            throw new Error(data.message);
        const securityCodeForm = document.getElementById("enter_code");
        const changePasswordForm = document.getElementById("change_password");
        changePasswordForm.classList.remove("hide");
        securityCodeForm.classList.add("hide");
        localStorage.setItem("verified", "True");
    })
        .catch((error) => {
        showError(error);
    });
}
function changePassword(password, confirm_password) {
    fetch("/change_password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            password: password,
            confirm_password: confirm_password,
            verified: localStorage.getItem("verified"),
            email: localStorage.getItem("recovery_email")
        }),
    })
        .then((response) => {
        return response.json();
    })
        .then((data) => {
        if (data.status === "failure")
            throw new Error(data.message);
        localStorage.removeItem("verified");
        localStorage.removeItem("email");
        resetForms();
    })
        .catch((error) => {
        showError(error);
    });
}
document.addEventListener("DOMContentLoaded", () => {
    const recoverAccountForm = document.getElementById("recover_account");
    const securityCodeForm = document.getElementById("enter_code");
    const changePasswordForm = document.getElementById("change_password");
    securityCodeForm.classList.add("hide");
    changePasswordForm.classList.add("hide");
    recoverAccountForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const email = document.querySelector("#email");
        sendRecoverEmail(email.value);
    });
    securityCodeForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const securityCode = document.querySelector("input[name=security_code]");
        const code = parseInt(securityCode.value);
        if (isNaN(code))
            showError("Enter numeric values only");
        verifyCode(code);
    });
    changePasswordForm.addEventListener("submit", (event) => {
        event.preventDefault();
        const password = document.querySelector("input[name=password]");
        const confirm_password = document.querySelector("input[name=confirm_password]");
        changePassword(password.value, confirm_password.value);
    });
});
//# sourceMappingURL=recover_account.js.map