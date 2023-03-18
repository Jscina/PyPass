function checkStatus(data) {
    switch (data.status) {
        case "success":
            login();
            break;
        default:
            let error = document.getElementById("error_msg");
            if (error === null)
                return;
            error.innerText = data.message;
            break;
    }
}
function login() {
    fetch("/home", {
        method: "GET",
    })
        .then((response) => {
        return (window.location.href = response.url);
    })
        .catch((error) => {
        console.error("Error fetching data:", error);
    });
}
function addLoginEventListener() {
    const login_form = document.getElementById("login");
    if (login_form === null)
        return;
    login_form.addEventListener("submit", (event) => {
        event.preventDefault();
        const username = document.querySelector('input[name="username"]').value;
        const password = document.querySelector('input[name="password"]').value;
        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `username=${username}&password=${password}`,
        })
            .then((response) => response.json())
            .then((data) => {
            checkStatus(data);
        })
            .catch((error) => {
            console.log(error);
        });
    });
}
window.addEventListener("load", addLoginEventListener);
//# sourceMappingURL=login.js.map