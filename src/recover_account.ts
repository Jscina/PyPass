function showError(error: string): void {
  const error_msg = document.querySelector(".error-msg") as HTMLDivElement;
  error_msg.classList.remove("hide");
  error_msg.innerHTML = `<p>${error}</p>`;
}

function resetForms(): void {
  const recoverAccountForm = document.getElementById(
    "recover_account"
  ) as HTMLFormElement;
  const securityCodeForm = document.getElementById(
    "enter_code"
  ) as HTMLFormElement;
  const changePasswordForm = document.getElementById(
    "change_password"
  ) as HTMLFormElement;

  recoverAccountForm.classList.remove("hide");
  securityCodeForm.classList.add("hide");
  changePasswordForm.classList.add("hide");
}

function sendRecoverEmail(email: string): void {
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
      const recoverAccountForm = document.getElementById(
        "recover_account"
      ) as HTMLFormElement;
      const securityCodeForm = document.getElementById(
        "enter_code"
      ) as HTMLFormElement;
      recoverAccountForm.classList.add("hide");
      securityCodeForm.classList.remove("hide");
    })
    .catch((error: string) => {
      showError(error);
    });
}

function verifyCode(securityCode: number): void {
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
      if (data.status === "failure") throw new Error(data.message);
      const securityCodeForm = document.getElementById(
        "enter_code"
      ) as HTMLFormElement;
      const changePasswordForm = document.getElementById(
        "change_password"
      ) as HTMLFormElement;
      changePasswordForm.classList.remove("hide");
      securityCodeForm.classList.add("hide");
      localStorage.setItem("verified", "True");
    })
    .catch((error: string) => {
      showError(error);
    });
}

function changePassword(password: string, confirm_password: string): void {
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
      if (data.status === "failure") throw new Error(data.message);
      localStorage.removeItem("verified");
      localStorage.removeItem("email");
      resetForms();
    })
    .catch((error: string) => {
      showError(error);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const recoverAccountForm = document.getElementById(
    "recover_account"
  ) as HTMLFormElement;
  const securityCodeForm = document.getElementById(
    "enter_code"
  ) as HTMLFormElement;
  const changePasswordForm = document.getElementById(
    "change_password"
  ) as HTMLFormElement;

  securityCodeForm.classList.add("hide");
  changePasswordForm.classList.add("hide");

  recoverAccountForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const email = document.querySelector("#email") as HTMLInputElement;
    sendRecoverEmail(email.value);
  });

  securityCodeForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const securityCode = document.querySelector(
      "input[name=security_code]"
    ) as HTMLInputElement;

    const code = parseInt(securityCode.value);
    if (isNaN(code)) showError("Enter numeric values only");
    verifyCode(code);
  });

  changePasswordForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const password = document.querySelector(
      "input[name=password]"
    ) as HTMLInputElement;
    const confirm_password = document.querySelector(
      "input[name=confirm_password]"
    ) as HTMLInputElement;
    changePassword(password.value, confirm_password.value);
  });
});
