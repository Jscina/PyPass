//Set login value to false on page load
window.addEventListener('load', (event) => {     
    window.localStorage.setItem("Login", "false");
});


// Test the login credentials
function login() {
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword").value;
    window.localStorage.setItem("email", email);
    eel.login(email, password)(verifyLogin);
}

// Log the user in if the return is valid
function verifyLogin(auth){   
    // Store the active user if the return is valid
    const email = window.localStorage.getItem("email")
    if(auth){
        eel.store_active_user(email);
        eel.get_name(email)(redirectToLogin);
    } 
    else{
        window.localStorage.setItem("Login", "false");
        alert("Username or Password is incorrect");
    }
        
    
}
// Redirect's user to the home page
function redirectToLogin(name)
{
    console.log(name)
    window.localStorage.setItem("Name", name)
    window.localStorage.setItem("Login", "true");
    window.location.href = "index.html";
}

window.addEventListener("submit", validateCreateAccount);

// Validate the passwords before creating the account
function validateCreateAccount(event){
    // Get the user input
    const first_name = document.getElementById("inputFirstName").value;
    const last_name = document.getElementById("inputLastName").value;
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword");
    const passwordConfirm = document.getElementById("inputPasswordConfirm");
    const securityQuestion = document.getElementById("inputSecurity").value;
    const securityAnswer = document.getElementById("inputAnswer").value;

    // Check if passwords match
    if (password.value === passwordConfirm.value){
        passwordConfirm.setCustomValidity("");
        createLoginAccount(first_name, last_name, email, password.value, securityQuestion, securityAnswer);
    }
    else{
        passwordConfirm.setCustomValidity("Passwords do not match");
        passwordConfirm.reportValidity();
        event.preventDefault();
    }
}

//Create account in the database then send the return to the loginRedirect function
function createLoginAccount(first_name, last_name, email, password, securityQuestion, securityAnswer){
    eel.createAccount(first_name, last_name, email, password, securityQuestion, securityAnswer)(loginRedirect);
}

// If the account was created successfully redirect to the login page
function loginRedirect(redirect){
    if(redirect){
        window.location.href = "login.html";
    }
    else{
        alert("Failed to add user account");
    }
}