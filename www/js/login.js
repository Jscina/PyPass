function login() {
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword").value;

    result = eel.test(email, password)();

    if(result) 
        window.location.href = "index.html";
    else
        alert("Incorrect username or password");
}
