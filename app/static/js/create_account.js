function addCreateAccountEventListenter() {
    const create_account_form = document.getElementById("create_account");
    if (create_account_form === null)
        return;
    create_account_form.addEventListener("submit", (event) => {
        event.preventDefault();
        const username = document.querySelector('input[name="username"]').value;
        const email = document.querySelector('input[name="email"]').value;
        const password = document.querySelector('input[name="password"]').value;
        const confirm_password = document.querySelector('input[name="confirm_password"]').value;
        fetch("/create_account", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `username=${username}&email=${email}&password=${password}&confirm_password=${confirm_password}`
        })
            .then(response => {
            if (response.redirected)
                login();
            else
                return response.json();
        })
            .then(data => {
            if (data === undefined)
                return;
            if (data.status === "error") {
                const error_msg = document.getElementById("error_msg");
                error_msg.innerText = data.message;
            }
        })
            .catch(error => {
            console.log(error);
        });
    });
}
window.addEventListener("load", addCreateAccountEventListenter);
//# sourceMappingURL=create_account.js.map