interface LoginResponse {
  status: string;
  message: string;
}

function redirectToHomePage(): void {
  window.location.href = "/home";
}

function displayErrorMessage(message: string): void {
  let error = document.getElementById("error_msg");
  if (error === null) return;
  error.innerText = message;
}

function checkStatus(data: LoginResponse): void {
  console.log(data);
  switch (data.status) {
    case "success":
      redirectToHomePage();
      break;
    default:
      displayErrorMessage(data.message);
      break;
  }
}

function submitLoginForm(username: string, password: string): void {
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      checkStatus(data);
    })
    .catch((error) => {
      console.log(error);
    });
}

function handleLoginFormSubmit(event: Event): void {
  event.preventDefault();
  const username = document.querySelector(
    'input[name="username"]'
  ) as HTMLInputElement;
  const password = document.querySelector(
    'input[name="password"]'
  ) as HTMLInputElement;

  submitLoginForm(username.value, password.value);
}

function addLoginEventListener(): void {
  const login_form = document.getElementById("login") as HTMLFormElement;
  if (login_form === null) return;
  login_form.addEventListener("submit", handleLoginFormSubmit);
}

window.addEventListener("load", addLoginEventListener);
