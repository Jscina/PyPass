function submitCreateAccountForm(event: Event): void {
  event.preventDefault();

  const createAccountData = getCreateAccountFormData();

  sendCreateAccountRequest(createAccountData)
    .then((response) => {
      if (response.redirected) redirectToHomePage();
      else return response.json();
    })
    .then(handleCreateAccountResponse)
    .catch((error) => {
      console.log(error);
    });
}

function getCreateAccountFormData(): { [key: string]: string } {
  const username = (
    document.querySelector('input[name="username"]') as HTMLInputElement
  ).value;
  const email = (
    document.querySelector('input[name="email"]') as HTMLInputElement
  ).value;
  const password = (
    document.querySelector('input[name="password"]') as HTMLInputElement
  ).value;
  const confirm_password = (
    document.querySelector('input[name="confirm_password"]') as HTMLInputElement
  ).value;

  return {
    username,
    email,
    password,
    confirm_password,
  };
}

function sendCreateAccountRequest(data: {
  [key: string]: string;
}): Promise<Response> {
  return fetch("/create_account", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
}

function handleCreateAccountResponse(data: any): void {
  if (data === undefined) return;
  if (data.status === "error") {
    const error_msg = document.getElementById("error_msg") as HTMLElement;
    error_msg.innerText = data.message;
  }
}

function addCreateAccountEventListenter(): void {
  const create_account_form = document.getElementById("create_account");
  if (create_account_form === null) return;
  create_account_form.addEventListener("submit", submitCreateAccountForm);
}

window.addEventListener("load", addCreateAccountEventListenter);
