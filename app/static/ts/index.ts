interface Account {
  website: string;
  account_name: string;
  account_username: string;
  account_password: string;
}

class User_Accounts implements Account {
  website: string;
  account_name: string;
  account_username: string;
  account_password: string;

  constructor(
    website: string,
    account_name: string,
    account_username: string,
    account_password: string
  ) {
    this.website = website;
    this.account_name = account_name;
    this.account_username = account_username;
    this.account_password = account_password;
  }
}

function toggle_sidebar(): void {
  const sidebar = document.getElementById("sidebar") as HTMLElement;
  const content = document.getElementById("content") as HTMLElement;
  const navmenu = document.getElementById("navmenu") as HTMLElement;

  if (sidebar.style.width === "250px") {
    sidebar.style.width = "0";
    content.classList.remove("shifted");
    navmenu.style.display = "block";
  } else {
    sidebar.style.width = "250px";
    content.classList.add("shifted");
    navmenu.style.display = "none";
  }
}

function buildAccountTable(accounts: Array<Account>): void {
  const table = document.getElementById("password_table") as HTMLTableElement;
  if (table === null) return;
  for (let index = 0; index < accounts.length; index++) {
    const row = table.insertRow(index + 1);
    const website = row.insertCell(0);
    const account_name = row.insertCell(1);
    const account_username = row.insertCell(2);
    const account_password = row.insertCell(3);
    website.innerHTML = accounts[index].website;
    account_name.innerHTML = accounts[index].account_name;
    account_username.innerHTML = accounts[index].account_username;
    account_password.innerHTML = accounts[index].account_password;
  }
}

function fetchUserAccounts(): Array<Account> | void {
  const accounts: Array<Account> = [];

  fetch("/fetch_accounts", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      // Check if the response is successful (status code 200-299)
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      console.log(response.json());
      return response.json();
    })
    .then((data) => {
      data.accounts.forEach((account: Account) => {
        accounts.push(
          new User_Accounts(
            account.website,
            account.account_name,
            account.account_username,
            account.account_password
          )
        );
      });
    })
    .catch((error) => {
      console.log(error);
      return;
    });
  return accounts;
}

window.onload = () => {
  const accounts = fetchUserAccounts();
  console.log(accounts);
};
