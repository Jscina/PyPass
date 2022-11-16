function getSecurityQuestion()
{
    const email = document.getElementById("inputResetEmail").value;
    window.localStorage.setItem("email", email);
    eel.get_security_question(email)(redirectToSecurity);
}

function redirectToSecurity(question)
{
    window.localStorage.setItem("question", question);
    window.location.href = "security.html";
}

function validate_answer()
{
    const email = window.localStorage.getItem("email")
    const answer = document.getElementById("inputSecurityAnswer").value;
    eel.get_security_answer(email, answer)(validate);
}

function validate(validated)
{
    if (validated)
        window.location.href = "reset-password.html";
    else
        alert("Answer to security question is wrong");
}
function validatePasswords()
{
    const password = document.getElementById("inputPassword");
    const passwordConfirm = document.getElementById("inputPasswordConfirm");
    if (password.value == passwordConfirm.value)
    {
        passwordConfirm.setCustomValidity("");
        resetPassword(password.value);
    }
    else
    {
        passwordConfirm.setCustomValidity("Passwords do not match");
        passwordConfirm.reportValidity();
        event.preventDefault();
    }
}

function resetPassword(password)
{
    const email = window.localStorage.getItem("email");
    eel.reset_password(password, email)(redirectLogin);
}

function redirectLogin(password_reset)
{
    if(password_reset)
        window.location.href = "login.html";
    else
        alert("Password reset failed");
}