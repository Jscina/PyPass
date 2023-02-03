// Contains the listeners for the create_account page
const create_account_btn = document.getElementById("create_account");

create_account_btn.addEventListener("click", () => {
    let python_data = $.get("/get_error_message");
    console.log(python_data);
    let data = JSON.parse(python_data);

    const error_msg = document.getElementById("error_msg");
    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const confirm_password = document.getElementById("confirm_password");
    
    error_msg.innerHTML = data["message"];
    username.style.borderColor = "#FFB6C1";
    password.style.borderColor = "#FFB6C1";
    confirm_password.borderColor = "#FFB6C1";
});