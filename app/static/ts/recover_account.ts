function submitRecoverAccountForm(event: Event): void {
  event.preventDefault();

  const recoverAccountData = getRecoverAccountFormData();

  sendRecoverAccountRequest(recoverAccountData)
    .then((response) => response.json())
    .then(checkStatus)
    .catch((error) => {
      console.log(error);
    });
}

function getRecoverAccountFormData(): { [key: string]: string } {
  const email = (
    document.querySelector('input[name="email"]') as HTMLInputElement
  ).value;
  const password = (
    document.querySelector('input[name="password"]') as HTMLInputElement
  ).value;
  const confirm_password = (
    document.querySelector(
      'input[name="confirm_password"]'
    ) as HTMLInputElement
  ).value;

  return {
    email,
    password,
    confirm_password,
  };
}

function sendRecoverAccountRequest(data: {
  [key: string]: string;
}): Promise<Response> {
  const formData = new URLSearchParams(data).toString();

  return fetch("/recover", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  });
}

function addRecoverAccountEventListener(): void {
  const recover_account_form = document.getElementById("recover_account");
  if (recover_account_form === null) return;
  recover_account_form.addEventListener("submit", submitRecoverAccountForm);
}

window.addEventListener("load", addRecoverAccountEventListener);
